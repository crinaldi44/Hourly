import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import serve_response
from domains.packages.services.package_service import Packages


def add_package(package):
    """Adds the specified package to the user's company.

        :return: None
    """
    employee, company, department, role = init_controller(permissions='post:packages')
    package["company_id"] = company
    validate_package = Packages.from_json(data=package)
    package_exists, _ = Packages.find(additional_filters={"name": package['name'], "company_id": company})
    if len(package_exists) > 0:
        raise HourlyException('err.hourly.PackageExists')
    Packages.add_row(validate_package)
    return serve_response(message="Success", status=201)
