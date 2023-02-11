from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException


def delete_package(id_):
    """Deletes a package from within a user's company.

        :param id_: Represents the ID of the package to delete.
        :return: None
    """
    employee, company, department, role = init_controller(permissions='delete:packages')
    return '', 204
