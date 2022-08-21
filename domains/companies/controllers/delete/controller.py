from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import serve_response
from domains.companies.services.company_service import Companies
from domains.departments.services.department_service import Departments


def delete_company():
    try:
        int(1)
    except:
        raise HourlyException('err.hourly.CompanyNotFound')

    company_match, count = Companies.find(id=1, include_totals=True)

    if count == 0:
        raise HourlyException('err.hourly.CompanyNotFound')
    else:
        try:
            Companies.delete_row(id=1)
        except Exception as E:
            # Company deletion has failed due to foreign key integrity checks.
            # Append names of departments to be deleted prior to company deletion.
            departments, department_count = Departments.find(company_id=1, include_totals=True)
            response_message = "Failed to delete company! Please delete the following " + str(
                department_count) + " department(s): "
            for department in departments:
                response_message += department["department_name"] + ','

            raise HourlyException('err.hourly.InvalidCompanyDelete',
                                  message=response_message,
                                  suggestion="Please ensure the company is cleared prior to deletion.")
        return serve_response(message="Successfully deleted company.", status=204)