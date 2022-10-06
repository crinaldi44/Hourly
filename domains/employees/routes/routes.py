from flask_cors import CORS
import bcrypt

from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import serve_response, ListResponse
from crosscutting.auth.authentication import token_required, validate_credentials
from flask import Blueprint, jsonify, request
from sqlalchemy import exc

from database.database import Session
from database.models import Department, Employee, Clockin
from domains.employees.services.employee_service import Employees

employees = Blueprint('employees', __name__, template_folder='templates', url_prefix='/api/v0')

CORS(employees)


# TODO: Encrypt password with passlib.
# TODO: All CRUD-type routes must be secured with JWT, with the exception of clockin.
# For this, we should check that the payload providing the employee id matches that of
# the department manager.


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
                except:
                    session.rollback()
                    raise HourlyException('err.hourly.UserNotFound')


# Obtains a summary of all payroll for a given pay period. A department
# can be specified to filter out this data.
@employees.get('/employees/payroll')
@token_required()
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
                payroll_sum += (clock_hours * value.department.pay_rate)

        # Return the generated payroll sum.
        return jsonify({'result': payroll_sum})


# Retrieves and returns hours
@employees.get('/employees/hours')
@token_required()
def get_hours():
    requested_department = request.args.get('department')

    with Session() as session:
        with session.begin():

            if requested_department is not None:
                result = session.query(Clockin).filter_by(department_id=requested_department).filter(
                    Clockin.clockout_time is not None)
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
