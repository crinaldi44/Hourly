import connexion

from crosscutting.auth.authentication import init_controller
from domains.clockins.services.clockin_service import clockin_service
from openapi_server.models import (
    CompanyListResponse, ClockinListResponse,
)
from domains.companies.services.company_service import Companies


def list_clockins():
    """
    List clockins.
    """

    _, _, department_id, _ = init_controller(permissions="get:clockins")

    items, total = clockin_service.list_rows(additional_filters={"department_id": department_id}, serialize=True)
    clockin_list_response = ClockinListResponse(clockins=items)

    if "include_totals" in connexion.request.args:
        return clockin_list_response, 200, {"X-Total-Count": total}

    return clockin_list_response, 200
