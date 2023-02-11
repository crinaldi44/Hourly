import bcrypt
import connexion

from crosscutting.auth.authentication import validate_credentials, init_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.core.db.database import Session
from domains.employees.services.employee_service import Employees
from models.role import Roles
from domains.companies.services.company_service import Companies
from domains.departments.services.department_service import Departments
from openapi_server.models import AddResponse, UserValidationListResponse


def authenticate_user():
    with Session() as session:
        with session.begin():
            return validate_credentials(session, connexion.request)


def add_employee(employee):
    """Posts a new employee to the models.

    :return: None
    """

    init_controller(permissions="post:employees")

    validate_employee = Employees.from_json(data=employee)
    validate_employee.password = bcrypt.hashpw(employee['password'].encode('utf-8'), bcrypt.gensalt()).decode()
    user_exists, _ = Employees.list_rows(additional_filters={"email": validate_employee.email})
    Roles.validate_exists(id=validate_employee.role_id)

    if len(user_exists) > 0:
        raise HourlyException('err.hourly.UserExists')

    employee = Employees.add_row(validate_employee)
    return AddResponse(id=employee.id), 201


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
    user_exists, _ = Employees.list_rows(additional_filters={"email": validate_employee.email})

    if len(user_exists) > 0:
        raise HourlyException('err.hourly.UserExists')

    employee = Employees.add_row(validate_employee)
    return AddResponse(id=employee.id), 201


def validate_employees(employee_validations):
    """Validates a list of employee validation models.

    :param employee_validations: Represents the employee validations list.
    :return: The validated list.
    """
    init_controller(permissions='validate:user')
    validations = employee_validations["employee_validations"]
    for i in range(0, len(validations)):
        Employees.validation_from_json(employee_validation=validations[i])
        email_exists, _ = Employees.list_rows(additional_filters={"email": validations[i]["email"]})
        validations[i]["is_email_valid"] = len(email_exists) == 0
        company_exists, _ = Companies.list_rows(additional_filters={"name": validations[i]['company_name']},
                                                serialize=True)
        if len(company_exists) == 0:
            validations[i]["is_company_valid"] = False
            validations[i]["is_department_valid"] = False
        else:
            validations[i]["is_company_valid"] = True
            validations[i]["company_id"] = company_exists[0]["id"]
            department_exists, _ = Departments.list_rows(additional_filters=
                                                         {"department_name": validations[i]['department_name'],
                                                          "company_id": company_exists[0]["id"]}, serialize=True)
            validations[i]["is_department_valid"] = len(department_exists) > 0
            if validations[i]["is_department_valid"]:
                validations[i]["department_id"] = department_exists[0]["id"]
        validations[i]["is_pay_rate_valid"] = True
        validations[i]["is_employee_valid"] = validations[i]["is_pay_rate_valid"] \
                                              and validations[i]["is_company_valid"] \
                                              and validations[i]["is_department_valid"] \
                                              and validations[i]["is_email_valid"]
    validation_list_response = UserValidationListResponse(userValidations=validations)
    return validation_list_response, 200
