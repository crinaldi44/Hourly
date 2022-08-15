from crosscutting.response.list_response import serve_response, ListResponse
from crosscutting.auth.authentication import token_required
from crosscutting.exception.hourly_exception import HourlyException
from flask_cors import CORS
from flask import Blueprint, request
from database.models import Package

# Represents the blueprint.
packages = Blueprint('packages', __name__, template_folder='templates', url_prefix='/api/v0')

# Enables Cross-Origin-Resource-Sharing across this domain.
CORS(packages)


@packages.get('/packages')
@token_required(init_payload_params=True)
def get_all_packages(_company_id, _role_id):
    """Retrieves all packages.

    :param _company_id: Represents the payload company ID.
    :param _role_id: Represents the payload role ID.
    :return: A list of packages.
    """
    search = request.args.to_dict()
    if _role_id <= 2:
        search["company_id"] = _company_id
    results, count = Package.query_table(**search)
    return ListResponse(records=results, total_count=count).serve()


@packages.get('/packages/<id>')
@token_required(init_payload_params=True)
def get_package_by_id(id, _company_id, _role_id):
    """Retrieves a package by ID.

    :param id: The ID of the package.
    :param _company_id: Represents the user's company id.
    :param _role_id: Represents the user's role id.
    :return: The package that matches the criteria.
    """

    query = {
        "id": id
    }
    if _role_id <= 2:
        query["company_id"] = _company_id
    result, count = Package.query_table(**query)

    if len(result) == 0:
        raise HourlyException('err.hourly.PackageNotFound')
    else:
        return ListResponse(records=result).serve()


@packages.post('/packages')
@token_required(init_payload_params=True)
def add_package(_company_id, _role_id):
    """Adds the specified package to the user's company.

    :param _company_id: Represents the user's company id.
    :param _role_id: Represents the user's role id.
    :return: None
    """
    data = request.get_json()
    package_exists, _ = Package.query_table(name=data['name'], company_id=_company_id)
    if len(package_exists) > 0:
        raise HourlyException('err.hourly.PackageExists')
    data["company_id"] = _company_id
    new_package = Package.validate_package(data=data)
    Package.add_row(new_package);
    return serve_response(message="Success", status=201)


@packages.delete('/packages/<package_id>')
@token_required(init_payload_params=True)
def delete_package(_company_id, _role_id, package_id):
    """Deletes a package from within a user's company.

    :param _company_id: Represents the user's company id.
    :param _role_id: Represents the user's role id.
    :param package_id: Represents the ID of the package to delete.
    :return: None
    """
    try:
        int(package_id)
    except:
        raise HourlyException('err.hourly.PackageNotFound')
    package_match, _ = Package.query_table(id=package_id, company_id=_company_id)

    if len(package_match) == 0:
        raise HourlyException('err.hourly.PackageNotFound')
    else:
        Package.delete_row(uid=package_id)
        return serve_response(message="Successfully deleted package.", status=204)
