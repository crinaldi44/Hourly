from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException


def delete_employee(id_):
    # If params are not specified, notify the user they messed up.
    employee, company, department, role = init_controller(permissions='delete:employees')
    return {}, 204
