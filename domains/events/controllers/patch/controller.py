from crosscutting.auth.authentication import init_controller
from crosscutting.response.list_response import serve_response
from domains.events.services.event_service import Events


def patch_event(id_, patch_document_list):
    """Patches an event.

    :param id_: Represents the id of the event.
    :param patch_document_list: Represents the list of patch documents.
    :return:
    """

    employee, company, department, role = init_controller(permissions='patch:events')

    Events.validate_exists(id=id_, in_company=company)
    Events.patch(uid=id_, patch_list=patch_document_list)

    return serve_response(status=204, message='')
