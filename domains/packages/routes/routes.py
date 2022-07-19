from crosscutting.response.response import serve_response
from database.utils import query_table
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
    results, count = query_table.query_table(Package, **request.args)
    response = results
    if count is not None:
        response = {
            "total_records": count,
            "records": results,
        }
    return serve_response(message="Success", status=200, data=response)


@packages.get('/packages/<id>')
@token_required
def get_package_by_id(id):
    result = query_table.query_table(Package, id=id)

    if len(result) == 0:
        raise HourlyException('err.hourly.PackageNotFound')
    else:
        return serve_response(message="Success", status=200, data=result)


@packages.post('/packages')
@token_required
def add_package():
    data = request.get_json()
    if not query_table.validate_model(Package, data):
        raise HourlyException('err.hourly.BadPackageFormatting')
    package_exists = query_table.query_table(Package, name=data['name'])
    if len(package_exists) > 0:
        raise HourlyException('err.hourly.PackageExists')
    query_table.add_row(Package, data);
    return serve_response(message="Success", status=201)


@packages.delete('/packages/<package_id>')
@token_required
def delete_package(package_id):
    try:
        int(package_id)
    except:
        raise HourlyException('err.hourly.PackageNotFound')
    package_match = query_table.query_table(Package, id=package_id)

    if len(package_match) == 0:
        raise HourlyException('err.hourly.PackageNotFound')
    else:
        query_table.delete_row(Package, uid=package_id)
        return serve_response(message="Successfully deleted package.", status=204)
