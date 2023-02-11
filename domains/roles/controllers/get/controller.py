import connexion

from crosscutting.exception.hourly_exception import HourlyException
from openapi_server.models import RoleListResponse


def list_roles():
    role_list_response = RoleListResponse(roles=[])
    if "include_totals" in connexion.request.args:
        return role_list_response, 200, {"X-Total-Count": role_list_response}
    return role_list_response, 200


def get_role(id):
    # result, count = Roles.find(id=id)

    if 1 == 0:
        raise HourlyException('err.hourly.RoleNotFound')
    else:
        return RoleListResponse(roles=[]), 200
