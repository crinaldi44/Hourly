import bcrypt
import connexion

from crosscutting.auth.authentication import validate_credentials, init_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import serve_response
from database.database import Session
from domains.employees.services.employee_service import Employees


def authenticate_user():
    with Session() as session:
        with session.begin():
            return validate_credentials(session, connexion.request)


def add_employee(employee):
    """Posts a new employee to the database.

    :return: None
    """

    validate_employee = Employees.from_json(data=employee)
    validate_employee.password = bcrypt.hashpw(employee['password'].encode('utf-8'), bcrypt.gensalt())
    user_exists, _ = Employees.find(additional_filters={"email": validate_employee.email})

    if len(user_exists) > 0:
        raise HourlyException('err.hourly.UserExists')

    Employees.add_row(validate_employee)
    return serve_response(message="Successfully added employee to the database!", status=201)


def signup_user(employee):
    """Registers a new employee to the user's company.

        :param employee: Represents the employee to add.
        :return: None
        """
    employee_id, company, department, role = init_controller(permissions='post:user')
    employee['company_id'] = company

    if role <= 2 and 'role_id' in employee:
        if employee['role_id'] > 2:
            employee['role_id'] = 1

    validate_employee = Employees.from_json(data=employee)
    validate_employee.password = bcrypt.hashpw(employee['password'].encode('utf-8'), bcrypt.gensalt())
    user_exists, _ = Employees.find(additional_filters={"email": validate_employee.email})

    if len(user_exists) > 0:
        raise HourlyException('err.hourly.UserExists')

    Employees.add_row(validate_employee)
    return serve_response(message='Success! Employee has been entered into the registry.', status=201)
