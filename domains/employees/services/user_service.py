import re
import bcrypt
from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.service.service import Service
import models.models
from openapi_server.models import User


class UserService(Service):

    def __init__(self) -> None:
        super().__init__(model=models.models.User, openapi_type=User, table_name="user")

    def _validate_user_email(email):
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')
        if not email or not re.fullmatch(email_regex, email):
            raise HourlyException("err.hourly.BadUsernameOrPassword", message="The email formatting is invalid.")

    def _validate_password(password):
        # TODO: Implement password checking.
        pass

    def validate_user_credentials(self, email, password):
        try:
            user = self.model.query.filter_by(email=email).all()
            pwd = password.encode('utf-8')
            check_pw = bcrypt.checkpw(password=pwd, hashed_password=user[0].password.encode('utf-8'))
            if len(user) == 0 or not check_pw:
                raise HourlyException("err.hourly.InvalidCredentials")
            else:
                return user[0]
        except Exception as E:
            print(E)
            raise HourlyException('err.hourly.InvalidCredentials')

    def signup_user(self, credentials, department_id=None):
        if department_id is None:
            raise HourlyException("err.hourly.DepartmentNotFound")
        user_exists = self.model.query.filter_by(email=credentials.email).all()
        if len(user_exists) > 0:
            raise HourlyException("err.hourly.UserExists")
        new_user = models.models.User(**credentials.to_dict())
        new_user.password = bcrypt.hashpw(credentials.password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        new_user.department_id = department_id
        self.add_row(row=new_user)
        return new_user


user_service = UserService()
