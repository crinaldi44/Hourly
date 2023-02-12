import connexion

from crosscutting.auth.authentication import init_controller
from domains.departments.services.department_service import DepartmentService
from openapi_server.models import DepartmentListResponse


def list_departments():
    employee_id, company_id, department_id, role_id = init_controller(permissions="get:departments")
    department_service = DepartmentService()
    departments, total = department_service.list_rows(**connexion.request.args)
    department_list_response = DepartmentListResponse(departments=departments)
    if "include_totals" in connexion.request.args:
        return department_list_response, 200, {"X-Total-Count": total}
    return department_list_response, 200


def get_department(id_):
    """Retrieves a department by ID.

    :param id_:
    :return: The department.
    """
    employee_id, company_id, department_id, role_id = init_controller(permissions="get:departments")
    department_service = DepartmentService()
    department = department_service.validate_exists(filters={"id": id_, "company_id": company_id})

    return DepartmentListResponse(departments=[department])
