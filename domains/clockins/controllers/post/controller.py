import datetime

from flask import jsonify

from crosscutting.auth.authentication import init_controller
from openapi_server.models import Clockin, PatchDocument


def add_clockin():
    """
    Add a new clockin.

    :param clockin:
    :return:
    """
    employee_id, _, department_id, _ = init_controller(permissions="get:clockins")

    return jsonify({"message": "You have been clocked in."})
