import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from domains.departments.services.department_service import DepartmentService
from openapi_server.models import Department, AddResponse


def add_department(department):
    init_controller(permissions="post:departments")
    new_department = Department(department)
    department_service = DepartmentService()
    rows, total = department_service.list_rows(additional_filters={"name": new_department.name})
    if total > 0:
        raise HourlyException("err.hourly.DepartmentExists")
    department_service.add_row(row=new_department)
    add_response = AddResponse(id=0)

    return add_response, 201
