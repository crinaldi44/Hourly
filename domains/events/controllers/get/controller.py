import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from domains.events.services.event_service import Events
from openapi_server.models import EventListResponse


def list_events():
    """Lists the events and returns them back to the user.

    :return: A list of event records.
    """

    employee, company, department, role = init_controller(permissions='get:events')

    search = connexion.request.args.to_dict()
    results, count = Events.list_rows(**search, additional_filters={"company_id": company}, serialize=True)
    event_list_response = EventListResponse(events=results)

    if "include_totals" in connexion.request.args:
        return event_list_response, 200, {"X-Total-Count": count}
    return event_list_response, 200


def get_event(id_):
    """Retrieves an event by ID.

    :param id_:
    :return: A response containing the event.
    """
    employee, company, department, role = init_controller(permissions='get:packages')

    result, count = Events.list_rows(additional_filters={"id": id_, "company_id": company}, serialize=True)

    if len(result) == 0:
        raise HourlyException('err.hourly.EventNotFound')
    else:
        return EventListResponse(events=result), 200
