from crosscutting.auth.authentication import initialize_controller
from crosscutting.response.list_response import serve_response
from domains.events.services.event_service import Events


def delete_event(id_):
    """Deletes an event from within a user's company.

        :param id_: Represents the ID of the event to delete.
        :return: None
    """
    employee, company, department, role = initialize_controller(permissions='delete:events')
    Events.validate_exists(id=id_, in_company=company)
    Events.delete_row(uid=id_)
    return serve_response(message="Successfully deleted event.", status=204)