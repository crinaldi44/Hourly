import connexion

from crosscutting.auth.authentication import init_controller, has_elevated_privileges
from domains.clockins.services.clockin_service import ClockinService
from openapi_server.models import (
    CompanyListResponse, ClockinListResponse,
)


def list_clockins():
    """
    List clockins.
    """

    employee_id, company_id, department_id, role_id = init_controller(permissions="get:departments")
    filters = None if has_elevated_privileges(role_id) else {"company_id"}
    clockin_service = ClockinService()
    clockins, total = clockin_service.list_rows(
                    q=connexion.request.args.get("q"),
                    limit=connexion.request.args.get("limit"),
                    offset=connexion.request.args.get("offset"),
                    additional_filters=filters)

    clockin_list_response = ClockinListResponse(clockins=clockins)

    if "include_totals" in connexion.request.args:
        return clockin_list_response, 200, {"X-Total-Count": total}

    return clockin_list_response, 200
