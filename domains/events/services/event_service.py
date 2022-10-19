from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.service.service import Service
from database.database import Session
from database.event import Event, EventSearch, EventModel


class EventService(Service):
    """Represents an Event Service.

    """

    def __init__(self):
        super().__init__(model=Event, schema=EventModel, table_name="Package")

    def search_events(self, query: EventSearch, company_id):
        """Searches events using the query set.
        """
        with Session() as session:
            with session.begin():
                results = session.query(self.model).filter(
                    self.model.start_datetime > query['from_date'],
                    self.model.end_datetime < query['to_date'],
                    self.model.company_id == company_id,
                    (self.model.package_id == query['package_id']) if 'package_id' in query else True).all()
                return [self.serialize(result) for result in results]


Events = EventService()
