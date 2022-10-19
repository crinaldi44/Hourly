from crosscutting.response.list_response import serve_response
from database.role import Roles


def delete_role():
    Roles.validate_role_exists(role_id=1)
    Roles.delete_row(id=1)
    return serve_response(message="Successfully deleted role.", status=204)