import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from openapi_server.models import AddResponse


def add_package(package):
    """Adds the specified package to the user's company.

        :return: None
    """
    # employee, company, department, role = init_controller(permissions='post:packages')
    # package["company_id"] = company
    # validate_package = Packages.from_json(data=package)
    # package_exists, _ = Packages.list_rows(additional_filters={"name": package['name'], "company_id": company})
    # if len(package_exists) > 0:
    #     raise HourlyException('err.hourly.PackageExists')
    # package = Packages.add_row(validate_package)
    return AddResponse(id=0), 201
