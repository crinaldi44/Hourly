import connexion
from crosscutting.auth.authentication import init_controller

from crosscutting.exception.hourly_exception import HourlyException
from domains.companies.services.company_service import CompanyService
from openapi_server.models import AddResponse, Company


def add_company(company):
    """Add a new company to the models.

    :return:
    """
    employee, company_id, department, role = init_controller(permissions='post:companies')
    company_service = CompanyService()
    new_company = Company.from_dict(company)
    exists, total = company_service.list_rows(additional_filters={"name": new_company.name})
    if total > 0:
        raise HourlyException("err.hourly.CompanyExists")
    company_service.add_row(row=new_company)
    add_response = AddResponse(id=0)
    return add_response, 201
