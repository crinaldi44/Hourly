import datetime

from flask import jsonify

from crosscutting.auth.authentication import init_controller
from domains.clockins.services.clockin_service import clockin_service
from openapi_server.models import Clockin, PatchDocument


def add_clockin():
    """
    Add a new clockin.

    :param clockin:
    :return:
    """
    employee_id, _, department_id, _ = init_controller(permissions="get:clockins")
    active_clockins, total = clockin_service.list_rows(additional_filters={"employee_id": employee_id, "out_time": None})
    clockin_datetime = datetime.datetime.now()
    if len(active_clockins) > 0:
        for clockin in active_clockins:
            patch_doc = PatchDocument(op="replace", path="/clockout_time", value=str(clockin_datetime))
            clockin_service.patch(uid=clockin.id, patch_list=[patch_doc])
            return jsonify({"message": "You have been clocked out."}), 200
    else:
        new_clockin = Clockin(in_time=clockin_datetime)
        clockin_service.add_row(row=new_clockin)

    return jsonify({"message": "You have been clocked in."})