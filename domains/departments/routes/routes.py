from database.utils import query_table

from domains.employees.employees import Department

from crosscutting.response.response import serve_response
from database.utils.query_table import query_table, add_row, delete_row, validate_model
from crosscutting.auth.authentication import token_required
from crosscutting.exception.hourly_exception import HourlyException
from flask_cors import CORS
from flask import Blueprint, request

# Represents the blueprint.
departments = Blueprint('departments', __name__, template_folder='templates')

# Enables Cross-Origin-Resource-Sharing across this domain.
CORS(departments)


@departments.get('/departments')
@token_required
def get_all_departments():
    results, count = query_table(Department, **request.args)
    response = results
    if count is not None:
        response = {
            "total_records": count,
            "records": results,
        }
    return serve_response(message="Success", status=200, data=response)


@departments.get('/departments/<id>')
@token_required
def get_department_by_id(id):
    result = query_table(Department, id=id)

    if len(result) == 0:
        raise HourlyException('err.hourly.DepartmentNotFound')
    else:
        return serve_response(message="Success", status=200, data=result)


@departments.post('/departments')
@token_required
def add_department():
    data = request.get_json()
    if not validate_model(Department, data):
        raise HourlyException('err.hourly.BadDepartmentFormatting')
    exists = query_table(Department, department_name=data['department_name'])
    if len(exists) > 0:
        raise HourlyException('err.hourly.DepartmentExists')
    else:
        add_row(Department, data);
    return serve_response(message="Success", status=201)


@departments.delete('/departments/<department_id>')
@token_required
def delete_department(department_id):
    try:
        int(department_id)
    except:
        raise HourlyException('err.hourly.DepartmentNotFound')

    department_match = query_table(Department, id=department_id)
    if len(department_match) == 0:
        raise HourlyException('err.hourly.DepartmentNotFound')
    else:
        if department_match[0].department_name == "Default Department" and department_match[0].id == 1:
            raise HourlyException('err.hourly.InvalidDepartmentDelete')
        try:
            delete_row(Department, uid=department_id)
        except:
            raise HourlyException('err.hourly.InvalidDepartmentDelete',
                                  message='The department contains employees!',
                                  suggestion='Please move all employees before deleting!')
        return serve_response(message="Successfully deleted department.", status=204)


