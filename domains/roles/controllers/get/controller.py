import connexion

from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import ListResponse
from database.role import Roles


def list_roles():
        results, count = Roles.find(**connexion.request.args, serialize=True)
        return ListResponse(records=results, total_count=count).serve()


def get_role(id):
    result, count = Roles.find(id=id)

    if count == 0:
        raise HourlyException('err.hourly.RoleNotFound')
    else:
        return ListResponse(records=result).serve()