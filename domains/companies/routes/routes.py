from crosscutting.response.list_response import serve_response, ListResponse
from crosscutting.auth.authentication import token_required
from crosscutting.exception.hourly_exception import HourlyException
from flask_cors import CORS
from flask import Blueprint, request

from database.models import Department
from domains.companies.services.company_service import Companies

companies = Blueprint('companies', __name__, template_folder='templates', url_prefix='/api/v0')

# Enables Cross-Origin-Resource-Sharing across this domain.
CORS(companies)


@companies.get('/companies')
@token_required(init_payload_params=True)
def get_all_companies(_company_id, _role_id):
    if _role_id <= 2:
        results, count = Companies.find(**request.args, id=_company_id, serialize=True)
    else:
        results, count = Companies.find(**request.args, serialize=True)
    return ListResponse(records=results, total_count=count).serve()


@companies.get('/companies/<id>')
@token_required()
def get_company_by_id(id):
    result, count = Companies.find(id=id, serialize=True)

    if len(result) == 0:
        raise HourlyException('err.hourly.CompanyNotFound')
    else:
        return ListResponse(records=result).serve()


@companies.post('/companies')
@token_required()
def add_company():
    validate_company = Companies.from_json(data=request.get_json())
    company_exists, _ = Companies.find(name=validate_company.name)
    if len(company_exists) > 0:
        raise HourlyException('err.hourly.CompanyExists')
    Companies.add_row(validate_company)
    return serve_response(message="Success", status=201)
