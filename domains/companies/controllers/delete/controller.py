from crosscutting.auth.authentication import init_controller
from crosscutting.exception.hourly_exception import HourlyException


def delete_company(id_):

    init_controller(permissions='delete:companies')

    return {}, 204
