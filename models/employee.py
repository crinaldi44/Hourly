import re

import bcrypt
from marshmallow import fields, validate, Schema
from marshmallow.validate import Length
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Integer, String, Float, ForeignKey, Boolean
from sqlalchemy.orm import relationship

from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.db.database import Base
from models.base import HourlyTable
from models.role import Roles
from models.company import Company, validate_company
from models.department import Department, validate_department


class Employee(HourlyTable, Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)
    email = Column(String(255), nullable=False)
    password = Column(String(255), nullable=False)
    first_name = Column(String(255), default='', nullable=False)
    last_name = Column(String(255), default='', nullable=False)
    pay_rate = Column(Float, default=0.0)
    title = Column(String(255), default="Employee")
    img_url = Column(String(255))
    department_id = Column(Integer(), ForeignKey('departments.id'), nullable=False)
    role_id = Column(Integer(), ForeignKey('roles.id'), default=1, nullable=False)
    company_id = Column(Integer(), ForeignKey('companies.id'), default=1)
    account_disabled = Column(Boolean(), default=False)

    department = relationship("Department")
    company = relationship("Company")
    role = relationship("Roles")

    # Represents the Employee as a dictionary, for serialization in JSON
    # response.
    def as_dict(self):
        return {
            'id': self.id,
            'email': self.email,
            'password': self.password,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'pay_rate': self.pay_rate,
            'title': self.title,
            'img_url': self.img_url,
            "role_id": self.role_id,
            "company_id": self.company_id,
            'department': self.department.as_dict(),
        }

    def profile_dict(self):
        """Represents this entity with additional profile information.

        :return: The profile, with additional company and role information.
        :rtype dict
        """
        profile = self.as_dict()
        profile.pop('company_id')
        profile.pop('role_id')
        profile.pop('password')
        profile["company"] = self.company.as_dict()
        profile["role"] = self.role.as_dict()
        return profile

    @classmethod
    def validate_employee(cls, data):
        """Validates the user credentials against a particular set of requirements. If
        the requirements match, returns True, else raises a particular HourlyException
        that corresponds with the issue. The criteria is as follows:

        1. The user's email is validated against a regular expression that will verify
            that the email is of the proper format.

        2. The user's password is validated against a regular expression that will verify
            that the password is of proper length and includes special characters.

        :return: A dict containing the user model as a JSON
        """
        data_keys = data.keys()
        email_regex = re.compile(r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Z|a-z]{2,})+')

        if 'email' not in data_keys or not isinstance(data['email'], str):
            raise HourlyException('err.hourly.BadUsernameOrPassword')

        if ('first_name' in data_keys and not isinstance(data['first_name'], str)) \
                or ('last_name' in data_keys and not isinstance(data['last_name'], str)):
            raise HourlyException('err.hourly.BadUserFormatting',
                                  message="Field 'name' is invalid, must be of type str.")

        # Validate the email and password against regex.
        if 'email' not in data_keys \
                or 'password' not in data_keys \
                or not re.fullmatch(email_regex, data['email']) \
                or not len(data['password']) >= 8:
            raise HourlyException('err.hourly.BadUsernameOrPassword')

        # If pay_rate provided, validate is a proper floating point value.
        if 'pay_rate' in data:
            try:
                data['pay_rate'] = float(data['pay_rate'])
            except Exception:
                raise HourlyException('err.hourly.InvalidUserPayRate')

        if 'department_id' not in data_keys or not isinstance(data['department_id'], int):
            raise HourlyException('err.hourly.DepartmentNotFound')

        if 'role_id' in data_keys:
            Roles.validate_role_exists(data['role_id'])

        Company.validate_company_exists(company_id=data['company_id'])
        Department.validate_department_exists(department_id=data['department_id'],
                                              in_company=data["company_id"])

        encrypt_password = bcrypt.hashpw(data['password'].encode('utf-8'), bcrypt.gensalt())

        # Destructure and return the values.
        return {
            "email": data['email'],
            "password": encrypt_password,
            "pay_rate": data["pay_rate"] if 'pay_rate' in data_keys else 0.0,
            "department_id": data['department_id'],
            "company_id": data["company_id"],
            "role_id": data["role_id"] if 'role_id' in data_keys else 1
        }

    # Represents a machine-readable representation of the state of the
    # Employee.
    def __repr__(self):
        return "<User(email='%s', password='%s', first_name='%s', role_id='%s', department='%s'" % (
            self.email, self.password, self.first_name, self.role_id, self.department_id
        )


class EmployeeModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        load_instance = True
        include_fk = True

    email = fields.Email()
    password = fields.Str(validate=Length(min=8, max=100), load_only=True,
                          error_messages={"length": "Length of field 'password' must be between 8 and 100 characters."})
    first_name = fields.Str(required=True, error_messages={"required": "Field 'first_name' is required!"})
    last_name = fields.Str(required=True)
    pay_rate = fields.Float(required=True, validate=validate.Range(min=0.00),
                            error_messages={"range": "Field 'pay_rate' must be a non-negative number."})
    title = fields.Str(validate=Length(max=50))
    department_id = fields.Integer(required=True, validate=validate_department,
                                   error_messages={"required": "Field 'department_id' is required for type Employee."})
    company_id = fields.Integer(validate=validate_company)


class EmployeeValidationModel(Schema):
    """
        Represents a model that can be used to validate employee
        validations.
    """
    first_name = fields.Str(required=True)
    last_name = fields.Str(required=True)
    email = fields.Str(required=True)
    department_name = fields.Str(required=True)
    pay_rate = fields.Float(default=0.0)
    company_name = fields.Str(required=True)
    company_id = fields.Integer()
    department_id = fields.Integer()
    is_employee_valid = fields.Bool(dump_default=False)
    is_email_valid = fields.Bool(dump_default=False)
    is_department_valid = fields.Bool(dump_default=False)
    is_company_valid = fields.Bool(dump_default=False)
    is_pay_rate_valid = fields.Bool(dump_default=False)


def validate_employee(employee_id):
    return Employee.validate_exists(id=employee_id)