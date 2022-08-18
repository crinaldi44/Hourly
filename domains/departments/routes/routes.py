from crosscutting.response.list_response import serve_response, ListResponse
from crosscutting.auth.authentication import token_required
from crosscutting.exception.hourly_exception import HourlyException
from flask_cors import CORS
from flask import Blueprint, request

from domains.departments.services.department_service import Departments

# Represents the blueprint for this domain.
departments = Blueprint('departments', __name__, template_folder='templates', url_prefix='/api/v0')

# Enables Cross-Origin-Resource-Sharing across this domain.
CORS(departments)


@departments.get('/departments')
@token_required(init_payload_params=True)
def get_all_departments(_company_id, _role_id):
    search = request.args.to_dict()
    if _role_id <= 2:
        search["company_id"] = _company_id
    results, count = Departments.find(**search, serialize=True)
    return ListResponse(records=results, total_count=count).serve()


@departments.get('/departments/<id>')
@token_required()
def get_department_by_id(id):
    result, _ = Departments.find(id=id)

    if len(result) == 0:
        raise HourlyException('err.hourly.DepartmentNotFound')
    else:
        return ListResponse(records=result).serve()


@departments.post('/departments')
@token_required(init_payload_params=True)
def add_department(_company_id, _role_id):
    data = request.get_json()
    data['company_id'] = _company_id
    Departments.from_json(data=data)

    exists, count = Departments.find(department_name=data["department_name"])
    if len(exists) > 0:
        raise HourlyException('err.hourly.DepartmentExists')
    else:
        Departments.add_row(data)
    return serve_response(message="Success", status=201)


@departments.delete('/departments/<department_id>')
@token_required(init_payload_params=True)
def delete_department(_company_id, _role_id, department_id):
    """Deletes a department within a company. Verifies that the company
    is within the user's company prior to deletion.

    :param _company_id:
    :param _role_id:
    :param department_id:
    :return:
    """

    department_match, _ = Departments.find(id=department_id)

    Departments.validate_department_exists(department_id=department_id, in_company=_company_id)

    try:
        Departments.delete_row(uid=department_id)
    except Exception as E:
        raise HourlyException('err.hourly.InvalidDepartmentDelete',
                              message='The department contains employees!',
                              suggestion='Please move all employees before deleting!')

    return serve_response(message="Successfully deleted department.", status=204)

