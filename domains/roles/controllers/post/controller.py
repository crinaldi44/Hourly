import connexion

from models.role import Roles


def add_role():
    validate_role = Roles.validate_model(connexion.request.get_json())
    Roles.add_row(validate_role)
    return '', 201
