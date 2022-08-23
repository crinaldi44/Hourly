import connexion

from crosscutting.auth.authentication import initialize_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import ListResponse
from domains.events.services.event_service import Events


def list_events():
    """Lists the events and returns them back to the user.

    :return: A list of event records.
    """

    employee, company, department, role = initialize_controller(permissions='get:events')

    search = connexion.request.args.to_dict()
    results, count = Events.find(**search, additional_filters={"company_id": company}, serialize=True)

    return ListResponse(records=results, total_count=count).serve()


def get_event(id_):
    """Retrieves an event by ID.

    :param id_:
    :return: A response containing the event.
    """
    employee, company, department, role = initialize_controller(permissions='get:packages')

    result, count = Events.find(additional_filters={"id": id_, "company_id": company}, serialize=True)

    if len(result) == 0:
        raise HourlyException('err.hourly.EventNotFound')
    else:
        return ListResponse(records=result).serve()
