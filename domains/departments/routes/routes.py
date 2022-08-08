from database.models import Department

from crosscutting.response.list_response import serve_response, ListResponse
from crosscutting.auth.authentication import token_required
from crosscutting.exception.hourly_exception import HourlyException
from flask_cors import CORS
from flask import Blueprint, request

# Represents the blueprint.
departments = Blueprint('departments', __name__, template_folder='templates', url_prefix='/api/v0')

# Enables Cross-Origin-Resource-Sharing across this domain.
CORS(departments)


@departments.get('/departments')
@token_required(init_payload_params=True)
def get_all_departments(_company_id, _role_id):
    search = request.args.to_dict()
    if _role_id <= 2:
        search["company_id"] = _company_id
    results, count = Department.query_table(**search)
    return ListResponse(records=results, total_count=count).serve()


@departments.get('/departments/<id>')
@token_required()
def get_department_by_id(id):
    result = Department.query_table(id=id)

    if len(result) == 0:
        raise HourlyException('err.hourly.DepartmentNotFound')
    else:
        return ListResponse(records=result).serve()


@departments.post('/departments')
@token_required(init_payload_params=True)
def add_department(_company_id, _role_id):
    data = request.get_json()
    data['company_id'] = _company_id
    if not Department.validate_model(row=data):
        raise HourlyException('err.hourly.BadDepartmentFormatting')
    exists, count = Department.query_table(department_name=data["department_name"])
    if len(exists) > 0:
        raise HourlyException('err.hourly.DepartmentExists')
    else:
        Department.add_row(data)
    return serve_response(message="Success", status=201)


@departments.delete('/departments/<department_id>')
@token_required(init_payload_params=True)
def delete_department(_company_id, _role_id, department_id):

    try:
        int(department_id)
    except:
        raise HourlyException('err.hourly.DepartmentNotFound')

    department_match, _ = Department.query_table(id=department_id)
    print(department_match)
    if len(department_match) == 0 or department_match[0]['company_id'] != _company_id:
        raise HourlyException('err.hourly.DepartmentNotFound')
    else:
        try:
            Department.delete_row(uid=department_id)
        except Exception as E:
            raise HourlyException('err.hourly.InvalidDepartmentDelete',
                                  message='The department contains employees!',
                                  suggestion='Please move all employees before deleting!')
        return serve_response(message="Successfully deleted department.", status=204)


