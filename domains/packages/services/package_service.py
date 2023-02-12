import models.models
from crosscutting.service.service import Service
from openapi_server.models import Package


class PackageService(Service):

    def __init__(self):
        super(PackageService, self).__init__(model=models.models.Package, openapi_type=Package, table_name="package")
