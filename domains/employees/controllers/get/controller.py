import connexion

from crosscutting.auth.authentication import initialize_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import ListResponse
from database.models import Employee
from domains.employees.services.employee_service import Employees


def list_users():
    """Retrieves the listing of all employees.

        :return: A list of all employees.
        """
    employee_id, company_id, department_id, role_id = initialize_controller(permissions='get:employees')
    search = connexion.request.args
    if role_id <= 2:
        results, count = Employees.find(**search, serialize=True, additional_filters={"company_id": company_id})
    else:
        results, count = Employees.find(**search, serialize=True)
    return ListResponse(records=results, total_count=count).serve()


def get_employee(id):
    """Retrieves an employee by id.

    :param id: Represents the ID of the employee.
    :return: The employee that matches the criteria.
    """
    employee_id, company_id, department_id, role_id = initialize_controller(permissions='get:employees')
    if role_id <= 2:
        result = Employees.find(additional_filters={"id": id, "company_id": company_id}, serialize=True)
    else:
        result = Employees.find(additional_filters={"id": id}, serialize=True)

    return ListResponse(records=result).serve()


def get_users_profile(id):
    """Retrieves a user's profile from within the database
    by joining the fields for their company and role IDs.

    This endpoint is primarily intended for use by organization
    owners and admins.

    :param user_id: Represents the ID of the profile.
    :return: The user's profile
    """
    result = Employees.get_users_profile(id)
    return ListResponse(result).serve()
