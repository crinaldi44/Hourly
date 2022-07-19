from database.utils import query_table

from domains.employees.employees import Clockin

from crosscutting.response.response import serve_response
from database.utils.query_table import query_table, delete_row
from crosscutting.auth.authentication import token_required
from crosscutting.exception.hourly_exception import HourlyException
from flask_cors import CORS
from flask import Blueprint, request

# Represents the blueprint.
clockins = Blueprint('clockins', __name__, template_folder='templates')

# Enables Cross-Origin-Resource-Sharing across this domain.
CORS(clockins)


@clockins.get('/clockins')
@token_required
def get_all_clockins():
    return serve_response(message="Success", status=200, data=query_table(Clockin, **request.args))


@clockins.get('/clockins/<id>')
@token_required
def get_clockin_by_id(id):
    result = query_table(Clockin, id=id)

    if len(result) == 0:
        raise HourlyException('err.hourly.ClockinNotFound')
    else:
        return serve_response(message="Success", status=200, data=result)


@clockins.delete('/clockins/<clockin_id>')
@token_required
def delete_clockin(clockin_id):
    try:
        int(clockin_id)
    except:
        raise HourlyException('err.hourly.ClockinNotFound')

    clockin_match = query_table(Clockin, id=clockin_id)
    if len(clockin_match) == 0:
        raise HourlyException('err.hourly.ClockinNotFound')
    else:
        delete_row(Clockin, uid=clockin_id)
        return serve_response(message="Successfully deleted clockin.", status=204)


