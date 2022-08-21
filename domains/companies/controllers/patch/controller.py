from crosscutting.auth.authentication import initialize_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import serve_response
from domains.companies.services.company_service import Companies


def patch_company(id_, patch_document_list):
    """Patches a company within the space.

    :param id: The id of the resource to patch.
    :param patch_document_list: Represents the list of RFC-6902 patch documents.
    :return:
    """
    employee, company, department, role = initialize_controller(permissions='patch:companies')
    if role <= 2 and int(id_) != company:
        raise HourlyException('err.hourly.CompanyNotFound')
    Companies.patch(uid=id_, patch_list=patch_document_list)

    return serve_response(status=204, message="Success.")