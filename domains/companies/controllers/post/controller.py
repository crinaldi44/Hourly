import connexion
from crosscutting.auth.authentication import init_controller

from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import serve_response
from domains.companies.services.company_service import Companies


def add_company(company):
    """Add a new company to the database.

    :return:
    """
    employee, company, department, role = init_controller(permissions='post:companies')
    request = connexion.request
    validate_company = Companies.from_json(data=request.get_json())
    company_exists, _ = Companies.find(additional_filters={"name": validate_company.name})
    if len(company_exists) > 0:
        raise HourlyException('err.hourly.CompanyExists')
    Companies.add_row(validate_company)
    return serve_response(message="Success", status=201)