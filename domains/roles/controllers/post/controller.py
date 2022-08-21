import connexion

from crosscutting.response.list_response import serve_response
from domains.roles.services.role_service import Roles


def add_role():
    validate_role = Roles.validate_model(connexion.request.get_json())
    Roles.add_row(validate_role)
    return serve_response(message="Success", status=201)