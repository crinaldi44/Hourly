from pickletools import float8
import sys
from email import message
from tkinter import E
from tokenize import Double, Floatnumber, Number
from unittest import result
from pymysql import IntegrityError

import sqlalchemy.exc
from auth.authentication import token_required
from flask import Flask, Blueprint, jsonify, request, session
from sqlalchemy import exc

from models.database import Session
from models.employees.employees import Department, Employee, Clockin

employees = Blueprint('employees', __name__, template_folder='templates')

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
    with Session() as session:
        with session.begin():

            department = request.args.get('department')

            # Query the database. If a department id is specified, filter by department.
            if not department is None:
                result = session.query(Employee).filter_by(department_id=int(department)).all()
            else:
                result = session.query(Employee).all()

            # For each element in the result set, convert to a 
            # dictionary.
            iterator = map(lambda res: res.as_dict(), result)

            # Return a JSONified list.
            return jsonify(list(iterator)), 200


# Retrieves an employee by their identifier.
@employees.get('/employees/<id>')
@token_required
def get_employee(id):
    with Session() as session:
        with session.begin():

            # Attempt to retrieve the employee corresponding to that ID and inner join
            # with their respective department.
            try: 
                result = session.query(Employee).filter_by(id=id).one()
            except exc.NoResultFound:
                return jsonify({'message': 'No employee found with that ID!'}), 404

            return jsonify(result.as_dict()), 200


@employees.post('/employees')
@token_required
def add_employee():
    # Store the data in a JSON object.
    data = request.get_json()

    # If the data could not be parsed as JSON or if it is too large,
    # notify the user.
    if data is None or len(request.get_data()) > 1000:
        return jsonify({'message': 'The content type must be provided as JSON or the request was too large.'}), 400

    # If any fields are missed, provide an error message.
    if not all(x in data.keys() for x in ['name', 'password', 'email', 'pay_rate', 'title', 'department_id']):
        print(str(data.keys()))
        return jsonify({'message': "Invalid employee specified! Perhaps you've forgotten a field."}), 400

    # Check that there is a first and a last name.
    if not len(str(data['name']).split(' ')) == 2:
        return jsonify({'message': 'Employee name must be at least, but no greater than, 2 space-separated strings.'}), 400

    with Session() as session:
        with session.begin():

            # Validate/verify that the department exists.
            try:
                departments = session.query(Department).filter_by(department_id=data['department_id']).one()
            except exc.NoResultFound:
                return jsonify({'message': 'Invalid department ID specified.'}), 404

            # Verify that we are specifying a valid type of pay rate.
            try:
                pay_rate = float(data['pay_rate'])
            except:
                return jsonify({'message': 'Invalid pay rate specified.'})

            empl = Employee(name=data['name'], password=data['password'], email=data['email'], 
            pay_rate=data['pay_rate'], title=data['title'], department_id=data['department_id'], covid_status='Healthy')

            session.add(empl)
            return jsonify({'message': 'Success'}), 201


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
            result = session.query(Employee).filter_by(id=id)
            if not result or result == []:
                return jsonify({'message': 'The requested resource was not found on the server!'}), 404
            else:
                session.query(Employee).filter_by(id=id).delete()
                return jsonify({'message': 'The resource has been deleted.'}), 204


# TODO: Implement patch request for employees on the database.
@employees.patch('/employees/<id>')
@token_required
def update_employee(id):

    with Session() as session:
        with session.begin():
            
            # Attempt to verify that employee exists and update
            try:
                session.query(Employee).filter_by(id=id).update(request.json)
            except IntegrityError as E:
                return jsonify({'message': 'No employee found with that ID.'}), 404

            
            return jsonify({'message': 'Success!'})



    return 'Not yet supported', 501


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
                        return jsonify({'message': 'No employee exists by that ID!'}), 404
                    session.add(Clockin(employee_id=id, department_id=active_employee.department_id))
                    session.commit()
                    return jsonify({'message': 'You have been successfully clocked in.'}), 201
                except exc.IntegrityError:
                    session.rollback()
                    return jsonify({'message': 'Employee with that ID does not exist!'}), 400


@employees.get('/employees/<id>/clockin')
@token_required
def get_clock_ins(id):
    with Session() as session:
        with session.begin():
            result = session.query(Clockin).filter_by(employee_id=id).all()
            if not result:
                return jsonify({'message': 'No clock-ins found for that employee.'}), 404
            else:
                iterator = map(lambda res: res.as_dict(), result)
                return jsonify(list(iterator)), 200


# Obtains clock-ins for each department.
@employees.get('/departments/<id>/clockin')
@token_required
def get_dept_clockins(id):
    with Session() as session:
        with session.begin():
            result = session.query(Clockin).filter_by(department_id=id).all()

            # If no clock-ins found, return an error.
            if not result:
                return jsonify({'message': 'No clockins found for that department.'}), 404
            else:
                list_result = map(lambda res: res.as_dict(), result)
                return jsonify(list(list_result)), 200


# Gets all departments.
@employees.get('/employees/departments')
@token_required
def get_departments():
    with Session() as session:
        with session.begin():
            result = session.query(Department).all()
            iterator = map(lambda res: res.as_dict(), result)
            return jsonify(list(iterator)), 200


# Adds a new department.
@employees.post('/employees/departments')
@token_required
def add_department():
        department = request.json

        if department is None or not all(x in department.keys() for x in ['department_name', 'manager_id']):
            return jsonify({'message': 'Invalid department provided! Please sure all fields are filled out!'}), 400
        else:
            with Session() as session:
                with session.begin():
                    
                    result = session.query(Department).filter_by(department_name=request.json['department_name']).all()

                    if len(result) > 0:
                        return jsonify({'message': 'Department with that name already exists.'})

                    dept = Department(department_name=request.json['department_name'], manager_id=request.json['manager_id'])
                    session.add(dept)
                    return jsonify({'message': 'Success'}), 201


# Gets a specified department by id.
@employees.get('/employees/departments/<id>')
def get_department(id):
    if not int(id):
        return jsonify({'message': 'Invalid department ID specified.'}), 400
    with Session() as session:
        with session.begin():
            result = session.query(Department).filter_by(department_id=id).first()
            if result is None:
                return jsonify({'message': 'Department id not found.'}), 404
            else:
                return jsonify(result.as_dict()) # Return the department.


# Deletes the specified department.
@employees.delete('/employees/departments/<id>')
def delete_department(id):
    if not int(id):
        return jsonify({'message': 'Invalid department ID specified.'}), 400
    with Session() as session:
        with session.begin():
            result = session.query(Department).filter_by(department_id=id)
            if result is None:
                return jsonify({'message': 'No department found with that ID!'}), 404
            else:
                try:
                    result.delete()
                except:
                    return jsonify({'message': 'The department contains employees! Please move all employees before deleting!'}), 400
                return jsonify({'message': 'Success!'}), 204


# Updates the specified employee.
@employees.patch('/employees/departments/<id>')
def update_department(id):
    if not int(id):
        return jsonify({'message': 'Invalid department ID specified.'}), 400
    with Session() as session:
        with session.begin():
            result = session.query(Department).filter_by(department_id=id)

            if result is None:
                return jsonify({'message': 'No department found with that ID!'}), 404
            else:
                try:
                    result.update(request.json)
                except:
                    return jsonify({'message': 'An error occurred!'}), 400
                else:
                    return jsonify({'message': 'Success!'}), 204


# Obtains a summary of all payroll for a given pay period. A department
# can be specified to filter out this data.
@employees.get('/employees/payroll')
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
                result = session.query(Clockin).filter_by(department_id=department).filter(Clockin.clockout_time != None).all()
            else: # Else, check all values
                result = session.query(Clockin).filter(Clockin.clockout_time != None).all()
            if not result: # If no result, 404 error
                        return jsonify({'message': 'No active clockins were found!'}), 404

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
def get_hours():
    
    requested_department = request.args.get('department')

    with Session() as session:
        with session.begin():

            if (requested_department is not None):
                result = session.query(Clockin).filter_by(department_id=requested_department).filter(Clockin.clockout_time != None)
            else:
                result = session.query(Clockin)
            
            result = result.all()

            if not result:
                return jsonify({'message': 'No clockins found!'}), 404
            else:
                hours_sum = 0

                for value in result:
                    clockin = value.clockout_time
                    clockout = value.clockout_time
                    clock_hours = float("{:.2f}".format((clockin - clockout).total_seconds() / 60 / 60))
                    hours_sum += clock_hours
                
                return jsonify({'result': hours_sum})

