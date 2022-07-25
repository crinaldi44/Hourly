from crosscutting.response.list_response import serve_response, ListResponse
from crosscutting.auth.authentication import token_required
from crosscutting.exception.hourly_exception import HourlyException
from flask_cors import CORS
from flask import Blueprint, request
from domains.employees.employees import Package

# Represents the blueprint.
packages = Blueprint('packages', __name__, template_folder='templates')

# Enables Cross-Origin-Resource-Sharing across this domain.
CORS(packages)


@packages.get('/packages')
@token_required
def get_all_packages():
    results, count = Package.query_table(**request.args)
    return ListResponse(records=results, total_count=count).serve()


@packages.get('/packages/<id>')
@token_required
def get_package_by_id(id):
    result, count = Package.query_table(id=id)

    if len(result) == 0:
        raise HourlyException('err.hourly.PackageNotFound')
    else:
        return ListResponse(data=result).serve()


@packages.post('/packages')
@token_required
def add_package():
    data = request.get_json()
    if not Package.validate_model(data):
        raise HourlyException('err.hourly.BadPackageFormatting')
    package_exists, _ = Package.query_table(name=data['name'])
    if len(package_exists) > 0:
        raise HourlyException('err.hourly.PackageExists')
    Package.add_row(data);
    return serve_response(message="Success", status=201)


@packages.delete('/packages/<package_id>')
@token_required
def delete_package(package_id):
    try:
        int(package_id)
    except:
        raise HourlyException('err.hourly.PackageNotFound')
    package_match = Package.query_table(id=package_id)

    if len(package_match) == 0:
        raise HourlyException('err.hourly.PackageNotFound')
    else:
        Package.delete_row(id=package_id)
        return serve_response(message="Successfully deleted package.", status=204)
