import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from domains.companies.services.company_service import Companies
from openapi_server.models import CompanyListResponse


def list_companies():
    request = connexion.request
    employee_id, company_id, department_id, role_id = init_controller(permissions="get:companies")

    if role_id <= 2:
        results, count = Companies.list_rows(**request.args, additional_filters={"id": company_id})
    else:
        results, count = Companies.list_rows(**request.args)
    company_list_response = CompanyListResponse(companies=results)
    if "include_totals" in connexion.request.args:
        return company_list_response, 200, {"X-Total-Count": count}
    return company_list_response, 200


def get_company(id_):
    """Retrieves a company by ID.

    :return:
    """
    result, count = Companies.validate_exists(filters={"id": id_})
    return CompanyListResponse(companies=result), 200
