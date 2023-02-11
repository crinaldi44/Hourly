import connexion

from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import ListResponse
from domains.companies.services.company_service import Companies


def list_companies():
    request = connexion.request
    employee_id, company_id, department_id, role_id = init_controller(permissions="get:companies")

    if role_id <= 2:
        results, count = Companies.list_rows(**request.args, serialize=True, additional_filters={"id": company_id})
    else:
        results, count = Companies.list_rows(**request.args, serialize=True)
    return ListResponse(records=results, total_count=count).serve()


def get_company(id_):
    """Retrieves a company by ID.

    :return:
    """
    result, count = Companies.list_rows(additional_filters={"id": id_}, serialize=True)

    if len(result) == 0:
        raise HourlyException('err.hourly.CompanyNotFound')
    else:
        return ListResponse(records=result).serve()
