from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.service.service import Service
from database.models import Employee
from database.schemas import EmployeeModel


class EmployeeService(Service):
    """Represents an Employee Service.

    """

    def __init__(self):
        super().__init__(model=Employee, schema=EmployeeModel, table_name="Employee")

    def get_users_profile(self, user_id):
        """Retrieves the user's profile by obtaining details regarding
        their respective department, company and role.

        :param user_id: The ID of the user to fetch the profile of.
        :return: A profile dict of the user's profile.
        """
        result, _ = self.find(id=user_id)
        if len(result) == 0:
            raise HourlyException('err.hourly.UserNotFound')
        return [result[0].profile_dict()]


Employees = EmployeeService()
