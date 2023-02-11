import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from openapi_server.models import EventListResponse


def list_events():
    """Lists the events and returns them back to the user.

    :return: A list of event records.
    """

    employee, company, department, role = init_controller(permissions='get:events')

    event_list_response = EventListResponse(events=[])

    if "include_totals" in connexion.request.args:
        return event_list_response, 200, {"X-Total-Count": 0}
    return event_list_response, 200


def get_event(id_):
    """Retrieves an event by ID.

    :param id_:
    :return: A response containing the event.
    """
    employee, company, department, role = init_controller(permissions='get:packages')

    return EventListResponse(events=[]), 200
