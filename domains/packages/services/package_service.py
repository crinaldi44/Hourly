from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.service.service import Service
from database.package import Package, PackageModel


class PackageService(Service):
    """Represents a Package Service.

    """

    def __init__(self):
        super().__init__(model=Package, schema=PackageModel, table_name="Package")

    def validate_package_exists(self, package_id, in_company=None):
        """Validates that the employee exists. If this condition
                is False, raises an error that corresponds to this model.

                :param package_id: Represents the id of the Package.
                :param in_company: Represents a company to check the package within.
                :return: A Bool representing whether the row exists.
                """
        if in_company is not None:
            result, count = self.find(id=package_id, company_id=in_company)
        else:
            result, count = self.find(id=package_id)

        if len(result) == 0:
            raise HourlyException('err.hourly.PackageNotFound')

        return result


Packages = PackageService()
