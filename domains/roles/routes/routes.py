from crosscutting.response.list_response import serve_response, ListResponse
from crosscutting.auth.authentication import token_required
from crosscutting.exception.hourly_exception import HourlyException
from flask_cors import CORS
from flask import Blueprint, request

# Represents the blueprint.
from domains.roles.services.role_service import Roles

roles = Blueprint('roles', __name__, template_folder='templates', url_prefix='/api/v0')

# Enables Cross-Origin-Resource-Sharing across this domain.
CORS(roles)

"""WARNING:

This resource maintains control of the Roles domain within the
cloud servers. Generally, Roles are intended to be a static resource,
and as sensitive data regarding access policies for all domains is 
contained within each row, no active users will be able to 
directly assume remote control over the contents of this domain.

Before making modifications to this domain, please consult with the
README, as there is generally a better way of going about most situations.
"""


@roles.get('/roles')
@token_required()
def get_all_roles():
    results, count = Roles.find(**request.args, serialize=True)
    return ListResponse(records=results, total_count=count).serve()


@roles.get('/roles/<id>')
@token_required()
def get_role_by_id(id):
    result, count = Roles.find(id=id)

    if count == 0:
        raise HourlyException('err.hourly.RoleNotFound')
    else:
        return ListResponse(records=result).serve()


@roles.post('/roles')
@token_required()
def add_role():
    validate_role = Roles.validate_model(request.get_json())
    Roles.add_row(validate_role)
    return serve_response(message="Success", status=201)


@roles.delete('/roles/<role_id>')
@token_required()
def delete_role(role_id):
    Roles.validate_role_exists(role_id=role_id)
    Roles.delete_row(id=role_id)
    return serve_response(message="Successfully deleted role.", status=204)
