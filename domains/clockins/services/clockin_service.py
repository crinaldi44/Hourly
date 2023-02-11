from crosscutting.service.service import Service
from models.clockin import Clockin, ClockinModel


class ClockinService(Service):

    def __init__(self):
        super(ClockinService, self).__init__(model=Clockin, schema=ClockinModel, table_name="Clockin")


clockin_service = ClockinService()
