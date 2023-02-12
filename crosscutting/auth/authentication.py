import connexion
from openapi_server.models.user_login_response import UserLoginResponse
from datetime import timedelta, datetime
import jwt

from crosscutting.core.config.config import config
from crosscutting.exception.hourly_exception import HourlyException
from domains.departments.services.department_service import DepartmentService
from domains.employees.services.user_service import UserService


def validate_credentials(session, req):
    """
    Validates user credentials and returns a token.

    :param session: Represents the current session.
    :param req: Represents the request.

    :return: token representation of the user
    """
    request = req.get_json()
    user_service = UserService()
    user = user_service.validate_user_credentials(email=request['email'], password=request['password'])
    department_service = DepartmentService()
    users_dept = department_service.validate_exists(filters={"id": user.department_id})
    token = generate_auth_token(user, company_id=users_dept.company_id)
    return UserLoginResponse(access_token=token), 200


def has_elevated_privileges(role):
    """
    Checks whether or not the user has elevated privileges.

    :param role:
    :return:
    """
    return role == 1


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

    return data["sub"], data["company_id"], data["department_id"], data["role"]["id"]


def generate_auth_token(user, company_id):
    """Generates an access token for the user.

    :param user: The user
    :return: An access token for the user
    """
    current_time_utc = datetime.utcnow()

    return jwt.encode({'department_id': user.department_id,
                       'company_id': company_id,
                       'name': user.first_name + ' ' + user.last_name,
                       'role': user.role.to_dict(),
                       'iat': current_time_utc,
                       'sub': user.id,
                       'iss': 'api.hourly.com',
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
