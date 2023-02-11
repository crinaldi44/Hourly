from datetime import datetime

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from domains.employees.services.employee_service import Employees
from domains.events.services.event_service import Events
from domains.packages.services.package_service import Packages
from openapi_server.models import AddResponse, EventListResponse


def add_event(event):
    """Adds a new event type with the specified package type
    to the company.

    :param event:
    :return:
    """

    employee, company, department, role = init_controller(permissions='post:events')

    validate_event = Events.from_json(event)
    validate_event.company_id = company

    if validate_event.start_datetime > validate_event.end_datetime:
        raise HourlyException('err.hourly.BadEventFormatting', message="Start date and time must be before end date!")

    Packages.validate_exists(id=validate_event.package_id, in_company=validate_event.company_id)

    if validate_event.employee_id is not None:
        Employees.validate_exists(id=validate_event.employee_id, in_company=validate_event.company_id)

    event = Events.add_row(validate_event)

    return AddResponse(id=event.id), 201


def search_events(search_query):
    """Searches events within the user's company using the specified criteria.
    """
    employee, company, department, role = init_controller(permissions="search:events")
    if 'package_name' in search_query.keys():
        package_exists, _ = Packages.list_rows(additional_filters={'name': search_query['package_name']})
        if len(package_exists) > 0:
            search_query['package_id'] = package_exists[0].id
        else:
            search_query['package_id'] = -1
    results = Events.search_events(query=search_query, company_id=company)
    event_list_response = EventListResponse(events=results)
    return event_list_response, 200
