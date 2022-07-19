from crosscutting.response.response import serve_response
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
    return serve_response(message="Success", status=200, data=query_table.query_table(Roles, **request.args))

@roles.get('/roles/<id>')
@token_required
def get_role_by_id(id):
    result = query_table.query_table(Roles, id=id)

    if len(result) == 0:
        raise HourlyException('err.hourly.RoleNotFound')
    else:
        return serve_response(message="Success", status=200, data=result)


@roles.post('/roles')
@token_required
def add_role():
    data = request.get_json()
    if not query_table.validate_model(Roles, data):
        raise HourlyException('err.hourly.BadRoleFormatting')
    query_table.add_row(Roles, data);
    return serve_response(message="Success", status=201)


@roles.delete('/roles/<role_id>')
@token_required
def delete_role(role_id):
    try:
        int(role_id)
    except:
        raise HourlyException('err.hourly.RoleNotFound')
    role_match = query_table.query_table(Roles, id=role_id)

    if len(role_match) == 0:
        raise HourlyException('err.hourly.RoleNotFound')
    else:
        query_table.delete_row(Roles, uid=role_id)
        return serve_response(message="Successfully deleted role.", status=204)
