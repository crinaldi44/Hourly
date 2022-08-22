from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.service.service import Service
from database.models import Event
from database.schemas import EventModel


class EventService(Service):
    """Represents an Event Service.

    """

    def __init__(self):
        super().__init__(model=Event, schema=EventModel, table_name="Package")


Events = EventService()
