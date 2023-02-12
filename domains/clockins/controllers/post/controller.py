import datetime

from flask import jsonify

from crosscutting.auth.authentication import init_controller
from domains.clockins.services.clockin_service import ClockinService
from openapi_server.models import Clockin, PatchDocument


def add_clockin():
    """
    Add a new clockin.

    :param clockin:
    :return:
    """
    employee_id, _, department_id, _ = init_controller(permissions="post:clockins")
    clockin_service = ClockinService()
    active_clockins, total = clockin_service.list_rows(
        additional_filters={"user_id": employee_id, "clockout_time": None})
    current_time = str(datetime.datetime.now())
    if total > 0:
        for clockin in active_clockins:
            clockin_service.patch(uid=clockin.id, patch_list=[{
                "op": "replace",
                "path": "/clockout_time",
                "value": current_time
            }])
    else:
        clockin_service.add_row(row=Clockin(clockin_time=current_time, user_id=employee_id))

    return jsonify({"result": f"You have been clocked {'out' if total > 0 else 'in'} at time {current_time}."})
