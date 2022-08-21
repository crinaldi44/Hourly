from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.service.service import Service
from database.database import Session
from database.models import Employee
from database.schemas import EmployeeModel


class EmployeeService(Service):
    """Represents an Employee Service.

    """

    def __init__(self):
        super().__init__(model=Employee, schema=EmployeeModel, table_name="Employee")

    def get_users_profile(self, user_id):
        """Retrieves the user's profile by obtaining details regarding
        their respective department, company and role. This service performs
        3 left joins and should be paired with a stricter rate limit and
        utilized for one resource at a time.

        :param user_id: The ID of the user to fetch the profile of.
        :return: A profile dict of the user's profile.
        """
        with Session() as session:
            with session.begin():
                result = session.query(self.model).filter_by(id=user_id).all()
                if len(result) == 0:
                    raise HourlyException('err.hourly.UserNotFound')
                return result[0].profile_dict()


Employees = EmployeeService()
