from crosscutting.service.service import Service
import models.models
from openapi_server.models import Company

class CompanyService(Service):

    def __init__(self) -> None:
        super().__init__(model=models.models.Company, openapi_type=Company, table_name="company")

user_service = CompanyService()
