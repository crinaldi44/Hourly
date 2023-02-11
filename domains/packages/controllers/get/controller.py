import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from domains.packages.services.package_service import Packages
from openapi_server.models import PackageListResponse


def list_packages():
    """Retrieves all packages.

        :param _company_id: Represents the payload company ID.
        :param _role_id: Represents the payload role ID.
        :return: A list of packages.
        """
    search = connexion.request.args.to_dict()
    employee, company, department, role = init_controller(permissions='get:packages')
    if role <= 2:
        results, count = Packages.list_rows(**search, additional_filters={"company_id": company}, serialize=True)
    else:
        results, count = Packages.list_rows(**search, serialize=True)
    package_list_response = PackageListResponse(packages=results)
    if "include_totals" in connexion.request.args:
        return package_list_response, 200, {"X-Total-Count": count}
    return package_list_response, 200


def get_package(id_):
    """Retrieves a package by ID.

        :param id_: The ID of the package.
        :return: The package that matches the criteria.
        """
    employee, company, department, role = init_controller(permissions='get:packages')
    query = {
        "id": id_
    }
    if role <= 2:
        query["company_id"] = company
    result, count = Packages.list_rows(additional_filters=query, serialize=True)

    if len(result) == 0:
        raise HourlyException('err.hourly.PackageNotFound')
    else:
        return PackageListResponse(packages=result), 200
