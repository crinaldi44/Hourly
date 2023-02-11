import connexion
from openapi_server.models import (
    CompanyListResponse,
)
from domains.companies.services.company_service import Companies


def list_clockins():
    """
    List clockins.
    """
    companies, _ = Companies.find(q=None, serialize=True)

    company_list_response = CompanyListResponse(data=companies, message="", status=200)

    if "include_totals" in connexion.request.args:
        return company_list_response, 200, {"X-Total-Count": len(companies)}

    return company_list_response, 200
