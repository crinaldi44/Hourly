from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import serve_response
from domains.packages.services.package_service import Packages


def delete_package(id_):
    """Deletes a package from within a user's company.

        :param id_: Represents the ID of the package to delete.
        :return: None
    """
    employee, company, department, role = init_controller(permissions='delete:packages')
    Packages.validate_exists(id=id_, in_company=company)
    try:
        Packages.delete_row(uid=id_)
    except Exception:
        raise HourlyException('err.hourly.InvalidPackageDelete', message="This package contains events!")
    return serve_response(message="Successfully deleted package.", status=204)