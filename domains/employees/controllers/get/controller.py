import connexion

from crosscutting.auth.authentication import init_controller
from openapi_server.models import UserListResponse, UserProfileResponse
from domains.employees.services.employee_service import Employees


def list_users():
    """Retrieves the listing of all employees.

        :return: A list of all employees.
        """
    employee_id, company_id, department_id, role_id = init_controller(permissions='get:employees')
    search = connexion.request.args
    if role_id <= 2:
        results, count = Employees.list_rows(**search, serialize=True, additional_filters={"company_id": company_id})
    else:
        results, count = Employees.list_rows(**search, serialize=True)
    user_list_response = UserListResponse(users=results)
    if "include_totals" in connexion.request.args:
        return user_list_response, 200, count
    return user_list_response, 200


def get_employee(id_):
    """Retrieves an employee by id.

    :param id_:
    :return: The employee that matches the criteria.
    """
    employee_id, company_id, department_id, role_id = init_controller(permissions='get:employees')
    if role_id <= 2:
        result = Employees.validate_exists(filters={"id": id_, "company_id": company_id})
    else:
        result = Employees.validate_exists(additional_filters={"id": id_})

    return UserListResponse(users=result), 200


def get_users_profile(id_):
    """Retrieves a user's profile from within the models
    by joining the fields for their company and role IDs.

    This endpoint is primarily intended for use by organization
    owners and admins as well as the user themselves.

    :param user_id: Represents the ID of the profile.
    :return: The user's profile
    """
    result = [Employees.get_users_profile(user_id=id_)]
    profile = Employees.get_users_profile(user_id=id_)
    user_profile_response = UserProfileResponse(userProfile=profile)
    return user_profile_response, 200
