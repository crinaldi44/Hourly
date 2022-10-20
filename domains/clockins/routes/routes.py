from models.clockin import Clockin

from crosscutting.response.list_response import serve_response, ListResponse
from crosscutting.auth.authentication import token_required
from crosscutting.exception.hourly_exception import HourlyException
from flask_cors import CORS
from flask import Blueprint, request

# Represents the blueprint.
clockins = Blueprint('clockins', __name__, template_folder='templates', url_prefix='/api/v0')

# Enables Cross-Origin-Resource-Sharing across this domain.
CORS(clockins)


@clockins.get('/clockins')
@token_required()
def get_all_clockins():
    results, count = Clockin.query_table(**request.args)
    if len(results) == 0:
        raise HourlyException('err.hourly.ClockinNotFound')
    return ListResponse(records=Clockin.query_table(**request.args), total_count=count).serve()


@clockins.get('/clockins/<id>')
@token_required()
def get_clockin_by_id(id):
    result = Clockin.query_table(id=id)

    if len(result) == 0:
        raise HourlyException('err.hourly.ClockinNotFound')
    else:
        return ListResponse(records=result).serve()


@clockins.delete('/clockins/<clockin_id>')
@token_required()
def delete_clockin(clockin_id):
    try:
        int(clockin_id)
    except:
        raise HourlyException('err.hourly.ClockinNotFound')

    clockin_match = Clockin.query_table(id=clockin_id)
    if len(clockin_match) == 0:
        raise HourlyException('err.hourly.ClockinNotFound')
    else:
        Clockin.delete_row(id=clockin_id)
        return serve_response(message="Successfully deleted clockin.", status=204)


