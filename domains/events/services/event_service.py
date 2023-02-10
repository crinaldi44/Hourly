import datetime

from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.service.service import Service
from crosscutting.db.database import Session
from models.event import Event, EventSearch, EventModel


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
                try:
                    to_date_str = datetime.datetime.strptime(query['to_date'], "%m/%d/%Y").date()
                    from_date_str = datetime.datetime.strptime(query['from_date'], "%m/%d/%Y").date()
                except:
                    raise HourlyException('err.hourly.InvalidEventSearch',
                                          message='Params from_date and to_date be of form dd/mm/YYYY!')
                if (to_date_str - from_date_str).days > 90:
                    raise HourlyException('err.hourly.InvalidEventSearch',
                                          message="Must not be >90 days between from_date and to_date!")
                results = session.query(self.model).filter(
                    self.model.start_datetime > query['from_date'],
                    self.model.end_datetime < query['to_date'],
                    self.model.company_id == company_id,
                    (self.model.package_id == query['package_id']) if 'package_id' in query else True).all()
                return [self.serialize(result) for result in results]


Events = EventService()
