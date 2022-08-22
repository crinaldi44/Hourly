import connexion

from crosscutting.auth.authentication import initialize_controller
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