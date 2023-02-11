import connexion

from crosscutting.auth.authentication import init_controller
from openapi_server.models import (
    CompanyListResponse, ClockinListResponse,
)
from open_alchemy.models import Clockin


def list_clockins():
    """
    List clockins.
    """

    _, _, department_id, _ = init_controller(permissions="get:clockins")
    test = Clockin.query.all()

    clockin_list_response = ClockinListResponse(clockins=test)

    if "include_totals" in connexion.request.args:
        return clockin_list_response, 200, {"X-Total-Count": 0}

    return clockin_list_response, 200
