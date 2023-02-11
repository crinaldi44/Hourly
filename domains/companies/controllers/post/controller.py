import connexion
from crosscutting.auth.authentication import init_controller

from crosscutting.exception.hourly_exception import HourlyException
from openapi_server.models import AddResponse
from domains.companies.services.company_service import Companies


def add_company(company):
    """Add a new company to the models.

    :return:
    """
    employee, company, department, role = init_controller(permissions='post:companies')
    request = connexion.request
    validate_company = Companies.from_json(data=request.get_json())
    company_exists, _ = Companies.list_rows(additional_filters={"name": validate_company.name})
    if len(company_exists) > 0:
        raise HourlyException('err.hourly.CompanyExists')
    result = Companies.add_row(validate_company)
    add_response = AddResponse(id=result.id)
    return add_response, 201