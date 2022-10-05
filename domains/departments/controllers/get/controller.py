import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import ListResponse
from domains.departments.services.department_service import Departments


def list_departments():
    employee_id, company_id, department_id, role_id = init_controller(permissions="get:departments")
    search = connexion.request.args.to_dict()
    if role_id <= 2:
        filters = {
            "company_id": company_id
        }
        if role_id < 2:
            filters["department_id"] = department_id
        result, count = Departments.find(**search, additional_filters=filters, serialize=True)
    else:
        result, count = Departments.find(**search, additional_filters={"id": id}, serialize=True)
    return ListResponse(records=result, total_count=count).serve()


def get_department(id_):
    """Retrieves a department by ID.

    :param id: Represents the ID of the department.
    :return: The department.
    """
    employee_id, company_id, department_id, role_id = init_controller(permissions="get:departments")

    if role_id <= 2:
        filters = {
            "company_id": company_id,
            "id": id_
        }
        if role_id < 2:
            filters["department_id"] = department_id
        result, _ = Departments.find(additional_filters=filters, serialize=True)
    else:
        result, _ = Departments.find(additional_filters={"id": id_}, serialize=True)

    if len(result) == 0:
        raise HourlyException('err.hourly.DepartmentNotFound')
    else:
        return ListResponse(records=result).serve()