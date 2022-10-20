from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.service.service import Service
from models.role import Roles, RoleModel


class RolesService(Service):
    """Represents a Role Service.

    """

    def __init__(self):
        super().__init__(model=Roles, schema=RoleModel)

    def validate_role_exists(self, role_id):
        """Validates that the employee exists. If this condition
                is False, raises an error that corresponds to this model.

                :param role_id: Represents the id of the role.
                :return: A Bool representing whether the row exists.
                """
        result, count = self.find(id=role_id)

        if len(result) == 0:
            raise HourlyException('err.hourly.RoleNotFound')

        return result


Roles = RolesService()
