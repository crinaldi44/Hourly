from crosscutting.auth.authentication import init_controller


def patch_event(id_, patch_document_list):
    """Patches an event.

    :param id_: Represents the id of the event.
    :param patch_document_list: Represents the list of patch documents.
    :return:
    """

    employee, company, department, role = init_controller(permissions='patch:events')
    #
    # for patch_doc in patch_document_list:
    #     if patch_doc['path'] == '/package_id':
    #         Packages.validate_exists(id=patch_doc.value, in_company=company)
    # Events.validate_exists(id=id_, in_company=company)
    # Events.patch(uid=id_, patch_list=patch_document_list)

    return '', 204
