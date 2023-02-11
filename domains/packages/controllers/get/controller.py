import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from openapi_server.models import PackageListResponse


def list_packages():
    """Retrieves all packages.

        :param _company_id: Represents the payload company ID.
        :param _role_id: Represents the payload role ID.
        :return: A list of packages.
        """
    search = connexion.request.args.to_dict()
    employee, company, department, role = init_controller(permissions='get:packages')

    package_list_response = PackageListResponse(packages=[])
    if "include_totals" in connexion.request.args:
        return package_list_response, 200, {"X-Total-Count": 0}
    return package_list_response, 200


def get_package(id_):
    """Retrieves a package by ID.

        :param id_: The ID of the package.
        :return: The package that matches the criteria.
        """
    employee, company, department, role = init_controller(permissions='get:packages')

    return PackageListResponse(packages=[]), 200
