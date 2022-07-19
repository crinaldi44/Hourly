from flask_cors import CORS
from pymysql import IntegrityError

from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.response import serve_response
from crosscutting.auth.authentication import token_required, protected_filter, validate_credentials
from flask import Blueprint, jsonify, request
from sqlalchemy import exc
from database.utils import query_table

from database.database import Session
from domains.employees.employees import Department, Employee, Clockin
from domains.employees.utils.utils import validate_user_model

employees = Blueprint('employees', __name__, template_folder='templates')

CORS(employees)


# TODO: Encrypt password with passlib.
# TODO: All CRUD-type routes must be secured with JWT, with the exception of clockin.
# For this, we should check that the payload providing the employee id matches that of
# the department manager.


# Gets all employees from the database. If GET is requested,
# queries the database and returns the instances of each 
# Employee model. Then, iterate over all instances, store
# the
@employees.get('/employees')
@token_required
def get_employees():
    results, count = query_table.query_table(Employee, **request.args)
    response = results
    if count is not None:
        response = {
            "total_records": count,
            "records": results,
        }
    return serve_response('Success', data=response, status=200)

# Retrieves an employee by their identifier.
@employees.get('/employees/<id>')
@token_required
def get_employee(id):
    result = query_table.query_table(Employee, id=id)
    if len(result) == 0:
        raise HourlyException('err.hourly.UserNotFound')
    else:
        return jsonify({'employees': result})


@employees.post('/employees')
@token_required
def add_employee():
    # Store the data in a JSON object.
    data = request.get_json()

    # If the data could not be parsed as JSON or if it is too large,
    # notify the user.
    if data is None or len(request.get_data()) > 1000:
        raise HourlyException('err.hourly.BadUserFormatting',
                              message='The content type must be provided as JSON or the request was too large.')

    validate_department = query_table.query_table(Department, id=data['department_id'])

    if len(validate_department) == 0:
        raise HourlyException('err.hourly.DepartmentNotFound')

    pay_rate = float(data['pay_rate'])  # Validate the pay rate is a valid float.
    query_table.add_row(Employee, data)
    return serve_response(message="Successfully added employee to the database!", status=201)


@employees.post('/employees/signup')
@token_required
def signup_employee():
    data = request.get_json()
    email, password, pay_rate, department_id = validate_user_model(data)

    new_employee = {"email": email, "password": password, "department_id": department_id, "role_id": 1,
                    "pay_rate": pay_rate}
    query_table.add_row(Employee, new_employee)
    return serve_response(message='Success! Employee has been entered into the registry.', status=201)


# Deletes an employee from the database.
@employees.delete('/employees/<id>')
@token_required
def delete_employee(id):
    # If params are not specified, notify the user they messed up.
    if not id:
        return jsonify({'message': 'Poorly formatted request!'}), 400

    # Context management with 'with' allows session to be dispatched and
    # released from memory once transaction has completed.
    with Session() as session:
        with session.begin():

            result = protected_filter(session, Employee).filter_by(id=id)

            if not result or result == []:
                return jsonify({'message': 'The requested resource was not found on the server!'}), 404
            else:
                session.query(Employee).filter_by(id=id).delete()
                return jsonify({'message': 'The resource has been deleted.'}), 204


# TODO: Implement patch request for employees on the database via patch document.
@employees.patch('/employees/<id>')
@token_required
def update_employee(id):
    with Session() as session:
        with session.begin():

            # Attempt to verify that employee exists and update
            try:
                protected_filter(session, Employee).filter_by(id=id).update(request.json)
            except IntegrityError as E:
                return jsonify({'message': 'No employee found with that ID.'}), 404

            return jsonify({'message': 'Success!'})

    return 'Not yet supported', 501


# Authenticates a user.
@employees.post('/employees/login')
def authenticate():
    if 'email' not in request.json['data'].keys() or 'password' not in request.json['data'].keys():
        raise HourlyException('err.hourly.InvalidCredentials')
    else:
        with Session() as session:
            with session.begin():
                return validate_credentials(session, request)


# Clocks an employee in. The flow of control will be
# that a post request is made without any content,
# specifying the employee id in the path params.
@employees.post('/employees/<id>/clockin')
def log_time(id):
    # Validate & verify the most recent time clock
    # without a clock out time. If none exists, create
    # a new one.
    with Session() as session:
        with session.begin():

            try:
                int(id)
            except:
                return jsonify({'message': 'An error occurred.'})

            result_query_set = session.query(Clockin).filter_by(employee_id=id, clockout_time=None)
            result = result_query_set.all()
            if result:
                result_query_set.update({})  # On update, DBMS takes care of adjusting the clock-out time.
                return jsonify({'message': 'You have been successfully clocked out.'})
            else:
                try:  # Attempt to add the record. If the employee !exists, return an error.
                    try:
                        active_employee = session.query(Employee).filter_by(id=id).one()
                    except exc.NoResultFound as Ex:
                        print(Ex)
                        raise HourlyException('err.hourly.UserNotFound', message='No employee exists by that ID!')
                    session.add(Clockin(employee_id=id, department_id=active_employee.department_id))
                    session.commit()
                    return jsonify({'message': 'You have been successfully clocked in.'}), 201
                except exc.IntegrityError:
                    session.rollback()
                    raise HourlyException('err.hourly.UserNotFound')


# Obtains a summary of all payroll for a given pay period. A department
# can be specified to filter out this data.
@employees.get('/employees/payroll')
@token_required
def get_payroll():
    # Represents the department ID query string, if one is provided.
    department = request.args.get('department')

    # Represents the active employee.
    employee_arg = request.args.get('employee')

    # Check all values whose department matches one in query string.
    # IMPORTANT: Ensure that the value of clockout_time is ! None/NULL
    with Session() as session:
        with session.begin():
            if department is not None:
                result = session.query(Clockin).filter_by(department_id=department).filter(
                    Clockin.clockout_time != None).all()
            else:  # Else, check all values
                result = session.query(Clockin).filter(Clockin.clockout_time != None).all()
            if not result:  # If no result, 404 error
                raise HourlyException('err.hourly.NoClockinsFound')

            payroll_sum = 0

            # Generate one giant payroll sum, calculated
            # as clockin-clockout * hourly.
            for value in result:
                # Represents time between clockout and in as a timedelta.
                time_distance = value.clockout_time - value.clockin_time

                # Represents total hours on the clock.
                clock_hours = float("{:.2f}".format(time_distance.total_seconds() / 60 / 60))

                # Add to the accumulator variable.
                payroll_sum += (clock_hours * value.parent.pay_rate)

        # Return the generated payroll sum.
        return jsonify({'result': payroll_sum})


# Retrieves and returns hours
@employees.get('/employees/hours')
@token_required
def get_hours():
    requested_department = request.args.get('department')

    with Session() as session:
        with session.begin():

            if (requested_department is not None):
                result = session.query(Clockin).filter_by(department_id=requested_department).filter(
                    Clockin.clockout_time != None)
            else:
                result = session.query(Clockin)

            result = result.all()

            if not result:
                raise HourlyException('err.hourly.NoClockinsFound')
            else:
                hours_sum = 0

                for value in result:
                    clockin = value.clockout_time
                    clockout = value.clockout_time
                    clock_hours = float("{:.2f}".format((clockin - clockout).total_seconds() / 60 / 60))
                    hours_sum += clock_hours

                return jsonify({'result': hours_sum})


# Retrieves the budget for the specified department.
@employees.get('/employees/budget/<id>')
@token_required
def get_budget(id):
    with Session() as session:
        with session.begin():
            try:
                result = protected_filter(session, Department).filter_by(id=id).one()
            except exc.NoResultFound as E:
                raise HourlyException('err.hourly.DepartmentNotFound')
            return jsonify(result.get_budget())