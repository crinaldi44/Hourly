from models.role import Roles


def delete_role():
    Roles.validate_role_exists(role_id=1)
    Roles.delete_row(id=1)
    return '', 204
