import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from domains.companies.services.company_service import CompanyService
from openapi_server.models import CompanyListResponse


def list_companies():
    """ Retrieves the list of companies.

    Returns:
        company_list_response::CompanyListResponse

    """
    employee_id, company_id, department_id, role_id = init_controller(permissions="get:companies")
    company_service = CompanyService()
    companies, total = company_service.list_rows(
        q=connexion.request.args.get("q"),
        limit=connexion.request.args.get("limit"),
        offset=connexion.request.args.get("offset"),
        sort=connexion.request.args.get("sort"),
        fields=connexion.request.args.get("fields")
    )

    company_list_response = CompanyListResponse(companies=companies)
    if "include_totals" in connexion.request.args:
        return company_list_response, 200, {"X-Total-Count": total}
    return company_list_response, 200


def get_company(id_):
    """Retrieves a company by ID.

    :return:
    """
    employee_id, company_id, department_id, role_id = init_controller(permissions="get:companies")
    company_service = CompanyService()
    company = company_service.validate_exists(filters={"id": id_})
    return CompanyListResponse(companies=[company]), 200
