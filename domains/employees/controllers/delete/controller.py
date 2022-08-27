from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import serve_response
from domains.employees.services.employee_service import Employees


def delete_employee(id_):
    # If params are not specified, notify the user they messed up.
    employee, company, department, role = init_controller(permissions='delete:employees')
    Employees.validate_exists(id=id_, in_company=company)

    try:
        Employees.delete_row(uid=id_)
    except Exception as E:
        raise HourlyException('err.hourly.InvalidUserDelete')

    return serve_response(message="User successfully deleted.", status=200)