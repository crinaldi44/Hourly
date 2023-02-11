from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException


def patch_company(id_, patch_document_list):
    """Patches a company within the space.

    :param id_: The id of the resource to patch.
    :param patch_document_list: Represents the list of RFC-6902 patch documents.
    :return:
    """
    employee, company, department, role = init_controller(permissions='patch:companies')
    if role <= 2 and int(id_) != company:
        raise HourlyException('err.hourly.CompanyNotFound')

    return {}, 204
