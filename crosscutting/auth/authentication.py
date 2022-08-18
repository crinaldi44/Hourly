import json

import bcrypt
import sqlalchemy.exc
from flask import Blueprint, jsonify, request
from sqlalchemy.exc import NoResultFound
from datetime import timedelta, datetime
import jwt
from flask import current_app
from functools import wraps
from flask_cors import CORS

from crosscutting.exception.hourly_exception import HourlyException
from database.models import Employee
from database.database import Session
from domains.employees.services.employee_service import EmployeeService


def validate_credentials(session, req):
    """Validates user credentials.

    :param session: Represents the current session.
    :param req: Represents the request.
    :return: A token bearing the credentials of the user.
    """
    auth_req = req.json['data']

    employee_email = auth_req['email']

    # Check the provided employee ID.
    try:

        # Represents a stored instance of the employee's account.
        result = session.query(Employee).filter_by(email=employee_email).one()
    except NoResultFound as e:  # If no result found, inform the employee and deny the auth token.
        raise HourlyException('err.hourly.InvalidCredentials')
    else:

        encoded_pw = auth_req['password'].encode('utf-8')
        check_pw = bcrypt.checkpw(password=encoded_pw, hashed_password=result.as_dict()['password'].encode('utf-8'))

        # Verify the password.
        if check_pw:
            try:

                # Query the departments to verify that we either have a manager OR they belong to dept #1.
                # if result.as_dict()['department']['manager_id'] == result.as_dict()['id']:
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
                       'company_id': user.company_id,
                       'name': user.first_name + ' ' + user.last_name,
                       'role': user.role.as_dict(),
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
    if payload['department_id'] == 1:
        return session.query(model)
    else:
        return session.query(model).filter_by(department_id=payload['department_id'])


def token_required(init_payload_params=False):
    """Asserts that a token is required on the specified route.
    Wraps the function that routes the data and passes the token
    data into the function as parameters.

    :param init_payload_params: Represents whether the JWT credentials should
    be initialized in the request method params
    :return: None
    """

    def inner(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            token = None
            if 'Authorization' in request.headers:
                token = request.headers['Authorization'].split(' ')[1]
            else:
                raise HourlyException('err.hourly.UnauthorizedRequest')

            with Session() as session:
                with session.begin():
                    try:
                        data = jwt.decode(token, current_app.config['SECRET_KEY'], algorithms=["HS256"])

                        # Verify that the user exists.
                        try:
                            current_user = EmployeeService().validate_exists(id=data['employee_id'])

                            has_access = False
                            role_data = data["role"]["permissions"].split(',')
                            for i in range(0, len(role_data)):
                                method, route = role_data[i].split(':')
                                path = request.path.split('/')[3]
                                if route == path and (method == 'all' or method == request.method.lower()):
                                    has_access = True
                            if not has_access:
                                raise HourlyException('err.hourly.UnauthorizedRequest')

                        except sqlalchemy.exc.IntegrityError as E:
                            raise HourlyException('err.hourly.UserNotFound')

                    # time_passed = data['exp'] - datetime.utcnow()
                    # if time_passed > timedelta(minutes=30):
                    #    return jsonify({'message': 'Authentication token has expired.'}), 403
                    except jwt.exceptions.InvalidTokenError:
                        raise HourlyException('err.hourly.UnauthorizedRequest',
                                              message='Authorization token is expired or invalid. Please re-authenticate.')
            if init_payload_params is True:
                return func(_company_id=data['company_id'], _role_id=data['role']["id"], *args, **kwargs)
            return func(*args, **kwargs)

        return wrapper

    return inner
