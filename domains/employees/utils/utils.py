import string
import re

from sqlalchemy import exc

# Gets or creates the specified row in the table. The
# session arg represents the session factory object.
from crosscutting.exception.hourly_exception import HourlyException


def get_or_create(session_fact, model, **kwargs):
    with session_fact() as session:
        with session.begin():
            try:
                result = session.query(model).filter_by(**kwargs).one()
                return result
            except exc.NoResultFound as E:
                result = model(**kwargs)
                session.add(result)
                session.commit()
                return result


"""
    Validates the user credentials against a particular set of requirements. If
    the requirements match, returns True, else raises a particular HourlyException
    that corresponds with the issue. The criteria is as follows:
        
        1. The user's email is validated against a regular expression that will verify
            that the email is of the proper format.
            
        2. The user's password is validated against a regular expression that will verify
            that the password is of proper length and includes special characters.
    
    Returns:
        email, password -> the set containing the user's email and password
"""


def validate_user_model(data) -> string:
    data_keys = data.keys()
    email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

    if not 'email' in data_keys or not type(data['email'] == 'string'):
        raise HourlyException('err.hourly.BadUsernameorPassword')

    # Validate the email and password against regex.
    if 'email' not in data_keys \
            or 'password' not in data_keys \
            or not re.fullmatch(email_regex, data['email']) \
            or not len(data['password']) >= 8:
        raise HourlyException('err.hourly.BadUsernameOrPassword')

    # If pay_rate provided, validate is a proper floating point value.
    if 'pay_rate' in data_keys and not isinstance(data['pay_rate'], float):
        raise HourlyException('err.hourly.InvalidUserPayRate')

    if 'department_id' not in data_keys or not isinstance(data['department_id'], int):
        raise HourlyException('err.hourly.DepartmentNotFound')

    # Destructure and return the values.
    return data['email'], data['password'], data['pay_rate'] if 'pay_rate' in data_keys else 0.0, data[
        'department_id'], data['company_id'], data['role_id']
