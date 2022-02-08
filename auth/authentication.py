from email.headerregistry import HeaderRegistry
from flask import Flask, Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound
from datetime import timedelta, datetime
from app import app
import jwt

from models.employees.employees import Department, Employee
from models.database import Session

authentication = Blueprint('authentication', __name__, template_folder='templates')


# Validates user credentials, returns True or
# False depending on one or both of the following
# conditions:
#
# 1) The employee's department
#    manager ID is equal to the employee's ID OR
# 2) The employee is of the manager department.
def validate_credentials(session, req):
    employee_id = req.form['id']

    # Check the provided employee ID.
    try:
        result = session.query(Employee).filter_by(id=employee_id).one()
    except NoResultFound as e:  # If no result found, inform the employee and deny the auth token.
        print(e)
        return jsonify({'message': 'No employee found with that ID.'}), 404
    else:

        # Verify the password.
        if result.as_dict()['password'] == req.form['password']:
            try:
                # Query the departments to verify that we either have a manager OR they belong to dept #1.
                dept_query = session.query(Department).filter_by(id=result.as_dict()['department_id']).one()
                if dept_query.as_dict()['manager_id'] == result.as_dict()['id']:
                    return jsonify({'message': 'You would be authenticated.'}), 501
            except NoResultFound as e:
                return jsonify({'message': 'No department exists with that ID.'})
            else:
                return jsonify({'message': 'You do not have the correct privileges. Please contact HR.'})
        else:
            return jsonify({'message': 'Invalid employee ID or password.'})

# Defines a type of middleware decorator that validates against a token being
# provided in the request headers.
def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']

        if not token:
            return jsonify({'message': 'The required authorization token is missing.'}), 403
        
        try:
            data = jwt.decode(token, app.config['SECRET_KEY'], algorithms=["HS256"])
            current_user = Employee.query.filter_by(id=data['employee_id']).first()
            # Perform some logic here
        except:
            return jsonify({'message': 'Authorization token is invalid.'}), 403
        return func(*args, **kwargs)
    return decorator


# Authenticates a user.
@authentication.post('/login')
def authenticate():
    if not request.form['id'] or not request.form['password']:
        return jsonify({'message': 'Invalid request.'}), 400
    else:
        with Session() as session:
            with session.begin():
                return validate_credentials(session, request)
