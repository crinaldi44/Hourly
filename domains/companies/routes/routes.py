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


@companies.delete('/companies/<company_id>')
@token_required()
def delete_company(company_id):
    try:
        int(company_id)
    except:
        raise HourlyException('err.hourly.CompanyNotFound')

    company_match, count = Companies.find(id=company_id, include_totals=True)

    if count == 0:
        raise HourlyException('err.hourly.CompanyNotFound')
    else:
        try:
            Companies.delete_row(id=company_id)
        except Exception as E:
            # Company deletion has failed due to foreign key integrity checks.
            # Append names of departments to be deleted prior to company deletion.
            departments, department_count = Department.query_table(company_id=company_id, include_totals=True)
            response_message = "Failed to delete company! Please delete the following " + str(
                department_count) + " department(s): "
            for department in departments:
                response_message += department["department_name"] + ','

            raise HourlyException('err.hourly.InvalidCompanyDelete',
                                  message=response_message,
                                  suggestion="Please ensure the company is cleared prior to deletion.")
        return serve_response(message="Successfully deleted company.", status=204)
