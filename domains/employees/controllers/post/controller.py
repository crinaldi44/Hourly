import bcrypt
import connexion

from crosscutting.auth.authentication import validate_credentials, initialize_controller
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

    employee['password'] = bcrypt.hashpw(employee['password'].encode('utf-8'), bcrypt.gensalt())

    validate_employee = Employees.from_json(data=employee)
    user_exists, _ = Employees.find(email=validate_employee.email)

    if len(user_exists) > 0:
        raise HourlyException('err.hourly.UserExists')

    Employees.add_row(validate_employee)
    return serve_response(message="Successfully added employee to the database!", status=201)


def signup_user(employee):
    """Registers a new employee to the user's company.

        :param employee: Represents the employee to add.
        :return: None
        """
    employee_id, company, department, role = initialize_controller(permissions='post:employees')
    employee['company_id'] = company

    if role <= 2 and 'role_id' in employee:
        if employee['role_id'] > 2:
            employee['role_id'] = 1

    validate_employee = Employees.from_json(data=employee)
    user_exists, _ = Employees.find(email=validate_employee.email)

    if len(user_exists) > 0:
        raise HourlyException('err.hourly.UserExists')

    Employees.add_row(validate_employee)
    return serve_response(message='Success! Employee has been entered into the registry.', status=201)
