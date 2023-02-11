import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from openapi_server.models import CompanyListResponse


def list_companies():
    request = connexion.request
    employee_id, company_id, department_id, role_id = init_controller(permissions="get:companies")

    company_list_response = CompanyListResponse(companies=[])
    if "include_totals" in connexion.request.args:
        return company_list_response, 200, {"X-Total-Count": 0}
    return company_list_response, 200


def get_company(id_):
    """Retrieves a company by ID.

    :return:
    """
    return CompanyListResponse(companies=[]), 200
