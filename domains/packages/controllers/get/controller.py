import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import ListResponse
from domains.packages.services.package_service import Packages


def list_packages():
    """Retrieves all packages.

        :param _company_id: Represents the payload company ID.
        :param _role_id: Represents the payload role ID.
        :return: A list of packages.
        """
    search = connexion.request.args.to_dict()
    employee, company, department, role = init_controller(permissions='get:packages')
    if role <= 2:
        results, count = Packages.find(**search, additional_filters={"company_id": company}, serialize=True)
    else:
        results, count = Packages.find(**search, serialize=True)
    return ListResponse(records=results, total_count=count).serve()


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
    result, count = Packages.find(additional_filters=query, serialize=True)

    if len(result) == 0:
        raise HourlyException('err.hourly.PackageNotFound')
    else:
        return ListResponse(records=result).serve()
