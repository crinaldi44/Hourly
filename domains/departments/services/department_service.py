from crosscutting.service.service import Service
import models.models
from openapi_server.models import Department


class DepartmentService(Service):

    def __init__(self) -> None:
        super().__init__(model=models.models.Department, openapi_type=Department, table_name="department")


department_service = DepartmentService()
