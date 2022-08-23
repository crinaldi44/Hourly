from datetime import datetime

from crosscutting.auth.authentication import initialize_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import serve_response
from domains.employees.services.employee_service import Employees
from domains.events.services.event_service import Events
from domains.packages.services.package_service import Packages


def add_event(event):
    """Adds a new event type with the specified package type
    to the company.

    :param event:
    :return:
    """

    employee, company, department, role = initialize_controller(permissions='post:events')

    validate_event = Events.from_json(event)
    validate_event.company_id = company

    if validate_event.start_datetime > validate_event.end_datetime:
        raise HourlyException('err.hourly.BadEventFormatting', message="Start date and time must be before end date!")

    Packages.validate_exists(id=validate_event.package_id, in_company=validate_event.company_id)

    if validate_event.employee_id is not None:
        Employees.validate_exists(id=validate_event.employee_id, in_company=validate_event.company_id)

    Events.add_row(validate_event)

    return serve_response(status=201, message='Success')