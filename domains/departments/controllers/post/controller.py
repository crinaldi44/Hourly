import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException


def add_department(department):
    employee_id, company_id, department_id, role_id = init_controller(permissions="post:departments")

    return {}, 201
