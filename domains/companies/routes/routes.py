from crosscutting.response.list_response import serve_response, ListResponse
from crosscutting.auth.authentication import token_required
from crosscutting.exception.hourly_exception import HourlyException
from flask_cors import CORS
from flask import Blueprint, request
from domains.employees.employees import Company, Employee, Department

# Represents the blueprint.
companies = Blueprint('companies', __name__, template_folder='templates')

# Enables Cross-Origin-Resource-Sharing across this domain.
CORS(companies)


@companies.get('/companies')
@token_required
def get_all_companies():
    results, count = Company.query_table(**request.args)
    return ListResponse(records=results, total_count=count).serve()


@companies.get('/companies/<id>')
@token_required
def get_company_by_id(id):
    result, count = Company.query_table(id=id)

    if len(result) == 0:
        raise HourlyException('err.hourly.CompanyNotFound')
    else:
        return ListResponse(records=result).serve()


@companies.post('/companies')
@token_required
def add_company():
    data = request.get_json()
    if not Company.validate_model(data):
        raise HourlyException('err.hourly.BadCompanyFormatting')
    package_exists, count = Company.query_table(name=data['name'])
    if count > 0:
        raise HourlyException('err.hourly.CompanyExists')
    Company.add_row(data);
    return serve_response(message="Success", status=201)


@companies.delete('/companies/<company_id>')
@token_required
def delete_company(company_id):
    try:
        int(company_id)
    except:
        raise HourlyException('err.hourly.CompanyNotFound')

    company_match, count = Company.query_table(id=company_id,include_totals=True)

    if count == 0:
        raise HourlyException('err.hourly.CompanyNotFound')
    else:
        try:
            Company.delete_row(id=company_id)
        except:
            # Company deletion has failed due to foreign key integrity checks.
            # Append names of departments to be deleted prior to company deletion.
            departments, department_count = Department.query_table(company_id=company_id, include_totals=True)
            response_message = "Failed to delete company! Please delete the following " +  str(department_count) + " department(s): "
            for department in departments:
                response_message += department["department_name"] + ','

            raise HourlyException('err.hourly.InvalidCompanyDelete',
                  message=response_message,
                  suggestion="Please ensure the company is cleared prior to deletion.")
        return serve_response(message="Successfully deleted company.", status=204)
