from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.service.service import Service
from database.models import Employee
from database.schemas import EmployeeModel


class EmployeeService(Service):
    """Represents an Employee Service.

    """

    def __init__(self):
        super().__init__(model=Employee, schema=EmployeeModel, table_name="Employee")


Employees = EmployeeService()
