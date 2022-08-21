from crosscutting.auth.authentication import initialize_controller
from crosscutting.response.list_response import serve_response
from domains.packages.services.package_service import Packages


def delete_package(id_):
    """Deletes a package from within a user's company.

        :param id: Represents the ID of the package to delete.
        :return: None
    """
    employee, company, department, role = initialize_controller(permissions='delete:packages')
    Packages.validate_exists(id=id_, in_company=company)
    Packages.delete_row(uid=id_)
    return serve_response(message="Successfully deleted package.", status=204)