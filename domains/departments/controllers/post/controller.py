import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from domains.departments.services.department_service import Departments


def add_department(department):
    employee_id, company_id, department_id, role_id = init_controller(permissions="post:departments")
    department['company_id'] = company_id
    validate_department = Departments.from_json(data=department)

    exists, count = Departments.list_rows(additional_filters={"department_name": validate_department.department_name})
    if len(exists) > 0:
        raise HourlyException('err.hourly.DepartmentExists')
    else:
        Departments.add_row(validate_department)
    return {}, 201