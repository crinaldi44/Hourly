from crosscutting.auth.authentication import initialize_controller
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.response.list_response import serve_response
from domains.departments.services.department_service import Departments


def delete_department(id_):
    """Deletes a department within a company. Verifies that the company
        is within the user's company prior to deletion.

        :param _company_id:
        :param _role_id:
        :param department_id:
        :return:
        """
    employee, company, department, role = initialize_controller(permissions='delete:departments')
    Departments.validate_department_exists(department_id=id_, in_company=company)

    try:
        Departments.delete_row(uid=id_)
    except Exception as E:
        raise HourlyException('err.hourly.InvalidDepartmentDelete',
                              message='The department contains employees!',
                              suggestion='Please move all employees before deleting!')

    return serve_response(message="Successfully deleted department.", status=204)
    pass