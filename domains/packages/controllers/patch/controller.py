from crosscutting.auth.authentication import init_controller


def patch_package(id_, patch_document_list):
    """Initiates a patch operation on the specified
    package.

    :param id_: The ID of the package
    :param patch_document_list: The list of patch documents.
    :return:
    """

    # employee, company, department, role = init_controller(permissions='patch:packages')
    # Packages.validate_exists(id=id_, in_company=company)
    # Packages.patch(uid=id_, patch_list=patch_document_list)

    return '', 204
