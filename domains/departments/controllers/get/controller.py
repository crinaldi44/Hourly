import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from domains.departments.services.department_service import Departments
from openapi_server.models import DepartmentListResponse


def list_departments():
    employee_id, company_id, department_id, role_id = init_controller(permissions="get:departments")
    search = connexion.request.args.to_dict()
    if role_id <= 2:
        filters = {
            "company_id": company_id
        }
        if role_id < 2:
            filters["department_id"] = department_id
        result, count = Departments.list_rows(**search, additional_filters=filters, serialize=True)
    else:
        result, count = Departments.list_rows(**search, serialize=True)
    department_list_response = DepartmentListResponse(departments=result)
    if "include_totals" in connexion.request.args:
        return department_list_response, 200, {"X-Total-Count": count}
    return department_list_response, 200


def get_department(id_):
    """Retrieves a department by ID.

    :param id: Represents the ID of the department.
    :return: The department.
    """
    employee_id, company_id, department_id, role_id = init_controller(permissions="get:departments")

    if role_id < 2:
        result, _ = Departments.validate_exists(filters={"id": employee_id})
    else:
        result, _ = Departments.validate_exists(filters={"id": id_})

    if len(result) == 0:
        raise HourlyException('err.hourly.DepartmentNotFound')
    else:
        return DepartmentListResponse(departments=result)