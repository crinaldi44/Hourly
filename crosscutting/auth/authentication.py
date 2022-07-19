from flask import Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound
from datetime import timedelta, datetime
import jwt
from flask import current_app
from functools import wraps
from flask_cors import CORS

from crosscutting.exception.hourly_exception import HourlyException
from domains.employees.employees import Employee
from database.database import Session

authentication = Blueprint('authentication', __name__, template_folder='templates')

CORS(authentication)


# Validates user credentials, returns True or
# False depending on one or both of the following
# conditions:
#
# 1) The employee's department
#    manager ID is equal to the employee's ID OR
# 2) The employee is of the manager department.
def validate_credentials(session, req):
    auth_req = req.json['data']

    employee_id = auth_req['email']

    # Check the provided employee ID.
    try:

        # Represents a stored instance of the employee's account.
        result = session.query(Employee).filter_by(email=employee_id).one()
    except NoResultFound as e:  # If no result found, inform the employee and deny the auth token.
        raise HourlyException('err.hourly.UserNotFound')
    else:

        # Verify the password.
        if result.as_dict()['password'] == auth_req['password']:
            try:

                # Query the departments to verify that we either have a manager OR they belong to dept #1.
                if result.as_dict()['department']['manager_id'] == result.as_dict()['id']:
                    token = generate_auth_token(result)
                    return jsonify({'token': token}), 200

            except NoResultFound as e:
                raise HourlyException('err.hourly.DepartmentNotFound')
            else:
                raise HourlyException('err.hourly.UnauthorizedRequest')
        else:
            raise HourlyException('err.hourly.InvalidCredentials')


"""
    Generates an auth token for the specified user. Encodes a JSON Web Token
    with an expiration of the default length of time.
"""


def generate_auth_token(user: Employee):

    current_time_utc = datetime.utcnow()

    return jwt.encode({'employee_id': user.id,
                       'department_id': user.department_id,
                       'department_name': user.as_dict()['department']['department_name'],
                       'name': user.name,
                       'role': user.role_id,
                       'iat': current_time_utc,
                       'exp': current_time_utc + timedelta(**current_app.config['DEFAULT_JWT_EXPIRATION'])},
                      current_app.config['SECRET_KEY']),


# Filters the specified model based on the params specified in the JWT token.
# Note that routes must be wrapped with @token_required.
def protected_filter(session, model):
    token = None
    if 'x-access-tokens' in request.headers:
        token = request.headers['x-access-tokens']
        payload = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])
    else:
        return jsonify({'message': 'Token is missing or invalid.'})
    if payload['department_id'] == 1 and payload['department_name'] == 'Management':
        return session.query(model)
    else:
        return session.query(model).filter_by(department_id=payload['department_id'])


# Defines a type of middleware decorator that validates against a token being
# provided in the request headers.
def token_required(func):
    @wraps(func)
    def decorator(*args, **kwargs):
        token = None
        if 'x-access-tokens' in request.headers:
            token = request.headers['x-access-tokens']
        else:
            return jsonify({'message': 'The required authorization token is missing.'}), 403

        with Session() as session:
            with session.begin():
                try:
                    data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

                    # Verify that the user exists.
                    try:
                        current_user = session.query(Employee).filter_by(id=data['employee_id']).first()
                    except:
                        print(E)
                        return jsonify({'message': 'Authorization token provided is invalid.'}), 403

                # time_passed = data['exp'] - datetime.utcnow()
                # if time_passed > timedelta(minutes=30):
                #    return jsonify({'message': 'Authentication token has expired.'}), 403
                except:
                    return jsonify({'message': 'Authorization token is expired or invalid.'}), 403

        return func(*args, **kwargs)

    return decorator
