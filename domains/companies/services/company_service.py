from crosscutting.service.service import Service
from database.models import Company
from database.schemas import CompanyModel


class CompanyService(Service):
    """Represents a Company Service.

    """

    def __init__(self):
        super().__init__(model=Company, schema=CompanyModel, table_name="company")


Companies = CompanyService()
