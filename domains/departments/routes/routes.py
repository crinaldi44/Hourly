from database.utils import query_table

from domains.employees.employees import Department

from crosscutting.response.list_response import serve_response, ListResponse
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
    results, count = Department.query_table(**request.args)
    return ListResponse(records=results, total_count=count).serve()


@departments.get('/departments/<id>')
@token_required
def get_department_by_id(id):
    result = Department.query_table(id=id)

    if len(result) == 0:
        raise HourlyException('err.hourly.DepartmentNotFound')
    else:
        return ListResponse(records=result).serve()


@departments.post('/departments')
@token_required
def add_department():
    data = request.get_json()
    print(data)
    if not Department.validate_model(row=data):
        raise HourlyException('err.hourly.BadDepartmentFormatting')
    exists, count = Department.query_table(department_name=data["department_name"])
    if len(exists) > 0:
        raise HourlyException('err.hourly.DepartmentExists')
    else:
        Department.add_row(data)
    return serve_response(message="Success", status=201)


@departments.delete('/departments/<department_id>')
@token_required
def delete_department(department_id):

    try:
        int(department_id)
    except:
        raise HourlyException('err.hourly.DepartmentNotFound')

    department_match = Department.query_table(id=department_id)
    if len(department_match) == 0:
        raise HourlyException('err.hourly.DepartmentNotFound')
    else:
        if department_match[0].department_name == "Default Department" and department_match[0].id == 1:
            raise HourlyException('err.hourly.InvalidDepartmentDelete')
        try:
            Department.delete_row(id=department_id)
        except:
            raise HourlyException('err.hourly.InvalidDepartmentDelete',
                                  message='The department contains employees!',
                                  suggestion='Please move all employees before deleting!')
        return serve_response(message="Successfully deleted department.", status=204)


