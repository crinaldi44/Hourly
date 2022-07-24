from crosscutting.response.list_response import serve_response, ListResponse
from database.utils import query_table
from crosscutting.auth.authentication import token_required
from crosscutting.exception.hourly_exception import HourlyException
from flask_cors import CORS
from flask import Blueprint, request
from domains.employees.employees import Roles

# Represents the blueprint.
roles = Blueprint('roles', __name__, template_folder='templates')

# Enables Cross-Origin-Resource-Sharing across this domain.
CORS(roles)


@roles.get('/roles')
@token_required
def get_all_roles():
    results, count = Roles.query_table(**request.args)
    return ListResponse(records=results, total_count=count)


@roles.get('/roles/<id>')
@token_required
def get_role_by_id(id):
    result, count = Roles.query_table(id=id)

    if count == 0:
        raise HourlyException('err.hourly.RoleNotFound')
    else:
        return ListResponse(records=result)


@roles.post('/roles')
@token_required
def add_role():
    data = request.get_json()
    if not Roles.validate_model(data):
        raise HourlyException('err.hourly.BadRoleFormatting')
    Roles.add_row(data);
    return serve_response(message="Success", status=201)


@roles.delete('/roles/<role_id>')
@token_required
def delete_role(role_id):
    try:
        int(role_id)
    except:
        raise HourlyException('err.hourly.RoleNotFound')
    role_match, count = Roles.query_table(id=role_id)

    if count == 0:
        raise HourlyException('err.hourly.RoleNotFound')
    else:
        Roles.delete_row(id=role_id)
        return serve_response(message="Successfully deleted role.", status=204)
