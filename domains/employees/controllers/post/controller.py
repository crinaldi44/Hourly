import bcrypt
import connexion

from crosscutting.auth.authentication import validate_credentials, init_controller, has_elevated_privileges
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.core.db.database import Session
from openapi_server.models import AddResponse, UserValidationListResponse, UserValidation, UserSignUpRequest

from domains.companies.services.company_service import CompanyService
from domains.departments.services.department_service import DepartmentService
from domains.employees.services.user_service import UserService


def authenticate_user():
    with Session() as session:
        with session.begin():
            return validate_credentials(session, connexion.request)


def add_employee(employee):
    """Posts a new employee to the models.

    :return: None
    """

    init_controller(permissions="post:employees")
    user_service = UserService()
    new_user = user_service.signup_user(credentials=employee)
    # role_service.validate_exists(id=new_user.role_id)
    # company_service.validate_exists(id=new_user.company_id)

    return AddResponse(id=new_user.id), 201


def signup_user(employee):
    """Registers a new employee to the user's company.

        :param employee: Represents the employee to add.
        :return: None
        """
    employee_id, company, department, user_role = init_controller(permissions='post:user')

    user_service = UserService()
    new_user = UserSignUpRequest(**employee)
    if not has_elevated_privileges(role=user_role):
        new_user.role_id = 1
    result = user_service.signup_user(credentials=new_user, department_id=department)

    return AddResponse(id=result.id), 201


def validate_employees(employee_validations):
    """Validates a list of employee validation models.

    :param employee_validations: Represents the employee validations list.
    :return: The validated list.
    """
    init_controller(permissions='validate:users')
    validations = employee_validations["validations"]
    user_service = UserService()
    company_service = CompanyService()
    department_service = DepartmentService()
    result_validations = []
    for i in range(0, len(validations)):
        validation = UserValidation(**validations[i])
        email_exists, _ = user_service.list_rows(additional_filters={"email": validation.email})
        validation.is_email_valid = len(email_exists) == 0
        company_exists, _ = company_service.list_rows(additional_filters={"name": validation.company_name})
        if len(company_exists) == 0:
            validation.is_company_valid = False
            validation.is_department_valid = False
        else:
            validation.is_company_valid = True
            validation.company_id = company_exists[0].id
            department_exists, total_deps = department_service.list_rows(additional_filters=
                                                                         {"name": validation.department_name,
                                                                          "company_id": company_exists[0].id})
            validation.is_department_valid = total_deps > 0
            if validation.is_department_valid:
                validation.department_id = department_exists[0].id
        validation.is_pay_rate_valid = True
        validation.is_employee_valid = validation.is_pay_rate_valid \
                                       and validation.is_company_valid \
                                       and validation.is_department_valid \
                                       and validation.is_email_valid
        result_validations.append(validation)
    validation_list_response = UserValidationListResponse(validations=result_validations)
    return validation_list_response, 200
