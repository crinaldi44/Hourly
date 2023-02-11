import connexion
from crosscutting.auth.authentication import init_controller

from crosscutting.exception.hourly_exception import HourlyException
from openapi_server.models import AddResponse


def add_company(company):
    """Add a new company to the models.

    :return:
    """
    employee, company, department, role = init_controller(permissions='post:companies')
    request = connexion.request
    add_response = AddResponse(id=0)
    return add_response, 201
