import connexion

from crosscutting.auth.authentication import init_controller
from domains.employees.services.user_service import UserService
from openapi_server.models import UserListResponse, UserProfileResponse


def list_users():
    """Retrieves the listing of all employees.

        :return: A list of all employees.
        """
    employee_id, company_id, department_id, role_id = init_controller(permissions='get:employees')
    user_service = UserService()
    users, total = user_service.list_rows(**connexion.request.args)
    user_list_response = UserListResponse(users=users)
    if "include_totals" in connexion.request.args:
        return user_list_response, 200, {"X-Total-Count": total}
    return user_list_response, 200


def get_employee(id_):
    """Retrieves an employee by id.

    :param id_:
    :return: The employee that matches the criteria.
    """
    employee_id, company_id, department_id, role_id = init_controller(permissions='get:employees')

    return UserListResponse(users=[]), 200


def get_users_profile(id_):
    """Retrieves a user's profile from within the models
    by joining the fields for their company and role IDs.

    This endpoint is primarily intended for use by organization
    owners and admins as well as the user themselves.

    :param user_id: Represents the ID of the profile.
    :return: The user's profile
    """
    user_profile_response = UserProfileResponse(userProfile=[])
    return user_profile_response, 200
