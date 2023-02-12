from crosscutting.service.service import Service
import models.models
from openapi_server.models import Clockin


class ClockinService(Service):

    def __init__(self) -> None:
        super().__init__(model=models.models.Clockin, openapi_type=Clockin, table_name="clockin")


department_service = ClockinService()
