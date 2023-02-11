import bcrypt
import connexion
import sqlalchemy.exc
from flask import jsonify, request
from sqlalchemy.exc import NoResultFound
from datetime import timedelta, datetime
import jwt
from flask import current_app
from functools import wraps

from crosscutting.core.config.config import config
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.core.db.database import Session


# def validate_credentials(session, req):
#     """Validates user credentials.
#
#     :param session: Represents the current session.
#     :param req: Represents the request.
#     :return: A token bearing the credentials of the user.
#     """
#     auth_req = req.get_json()
#
#     employee_email = auth_req['email']
#
#     # Check the provided employee ID.
#     try:
#
#         # Represents a stored instance of the employee's account.
#         result = session.query(Employee).filter_by(email=employee_email).one()
#     except NoResultFound as e:  # If no result found, inform the employee and deny the auth token.
#         raise HourlyException('err.hourly.InvalidCredentials')
#     else:
#
#         encoded_pw = auth_req['password'].encode('utf-8')
#         check_pw = bcrypt.checkpw(password=encoded_pw, hashed_password=result.as_dict()['password'].encode('utf-8'))
#
#         # Verify the password.
#         if check_pw:
#             try:
#
#                 # Query the departments to verify that we either have a manager OR they belong to dept #1.
#                 # if result.as_dict()['department']['manager_id'] == result.as_dict()['id']:
#                 token = generate_auth_token(result)
#                 return jsonify({'accessToken': token}), 200
#
#             except NoResultFound as e:
#                 raise HourlyException('err.hourly.DepartmentNotFound')
#         else:
#             raise HourlyException('err.hourly.InvalidCredentials')

def validate_credentials(session, request):
    pass


def init_controller(permissions: str) -> tuple:
    """Initializes a controller by route permissions that
    can be found by decoding the user's access token and returning
    the role permissions mapping. If the user has permissions, will
    return a tuple containing their role, department, company id, and
    user id. Else, raises an exception routing their request back.

    :param permissions:
    :return: A tuple containing the user info in the payload.
    """
    token = connexion.request.headers['Authorization'].split(' ')[1]
    data = jwt.decode(token, config.JWT_SECRET_RANDOMIZED, algorithms=["HS256"])
    has_access = False
    role_data = data["role"]["permissions"].split(',')
    for i in range(0, len(role_data)):
        permission_data = role_data[i].split(':')
        perm_split = permissions.split(':')
        if role_data[i] == permissions or (permission_data[0] == 'all' and permission_data[1] == perm_split[1]):
            has_access = True
    if not has_access:
        raise HourlyException('err.hourly.UnauthorizedRequest')

    return data["employee_id"], data["company_id"], data["department_id"], data["role"]["id"]


def generate_auth_token(user):
    """Generates an access token for the user.

    :param user: The user
    :return: An access token for the user
    """
    current_time_utc = datetime.utcnow()

    return jwt.encode({'employee_id': user.id,
                       'department_id': user.department_id,
                       'company_id': user.company_id,
                       'name': user.first_name + ' ' + user.last_name,
                       'role': user.role.as_dict(),
                       'iat': current_time_utc,
                       'exp': current_time_utc + timedelta(**config.DEFAULT_JWT_EXPIRATION)},
                      config.JWT_SECRET_RANDOMIZED)


def validate_field_in_payload(token, field_name: str):
    """Validates that the designated field exists within
    the user's access token.

    :param token: The token
    :param field_name: The field name to check
    :return: The field, if it exists
    """
    return token[field_name]


def authenticate_user(token):
    """Authenticates a user. Validates the integrity of the access token
    against the general formatting and validates that the user making the
    request is still a valid user.

    :param token: The token
    :return: None
    """
    try:
        return jwt.decode(token, config.JWT_SECRET_RANDOMIZED, algorithms=['HS256'])
    except jwt.exceptions.InvalidTokenError:
        raise HourlyException('err.hourly.UnauthorizedRequest',
                              message="Access token is expired or invalid. Please re-authenticate.")
    # employee_id = validate_field_in_payload(result, "employee_id")
    # EmployeeService().validate_exists(id=employee_id)
    # validate_field_in_payload(result, "department_id")
    # validate_field_in_payload(result, "company_id")
    # validate_field_in_payload(result, "role")
