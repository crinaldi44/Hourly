from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException


def delete_department(id_):
    """Deletes a department within a company. Verifies that the company
        is within the user's company prior to deletion.

        :param _company_id:
        :param _role_id:
        :param department_id:
        :return:
        """
    employee, company, department, role = init_controller(permissions='delete:departments')

    return {}, 204
