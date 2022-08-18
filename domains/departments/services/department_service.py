from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.service.service import Service
from database.models import Department
from database.schemas import DepartmentModel


class DepartmentService(Service):
    """Represents a Company Service.

    """

    def __init__(self):
        super().__init__(model=Department, schema=DepartmentModel, table_name="Department")

    def validate_department_exists(self, department_id, in_company=None):
        """Validates that the department exists. If this condition
                is False, raises an error that corresponds to this model.

                :param department_id: Represents the id of the department.
                :param in_company: Represents a company to check the department within.
                :return: A Bool representing whether the row exists.
                """
        if in_company is not None:
            result, count = self.find(id=department_id, company_id=in_company)
        else:
            result, count = self.find(id=department_id)

        if len(result) == 0:
            raise HourlyException('err.hourly.DepartmentNotFound')

        return result


Departments = DepartmentService()
