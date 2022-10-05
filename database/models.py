from email.policy import default
import json
import re
from typing import List, Any

import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, Float, text, JSON, Boolean, Text
from sqlalchemy.orm import relationship

from crosscutting.exception.hourly_exception import HourlyException
from database.database import engine, Base, Session
from domains.employees.utils.utils import get_or_create

"""Represents the default number of rows per page for a user
   response.
"""
DEFAULT_LIMIT = 20

MAX_LIMIT = 100


class HourlyTable(object):
    """Represents a class whose primary function is to serve data to the user.
       The class is intended to be an extension of the Base to provide static
       functionality to the table objects.
    """

    @classmethod
    def validate_exists(cls, id, in_company=None, in_department=None, table_name="Company"):
        """Validates that the employee exists. If this condition
        is False, raises an error that corresponds to this model.

        :param table_name:
        :param in_department:
        :param id: Represents the id of the resource.
        :param in_company: Represents a company to check the resource within.
        :return: A Bool representing whether the row exists.
        """
        query = {
            "id": id
        }
        if in_company is not None:
            query["company_id"] = in_company
        if in_department is not None:
            query["department_id"] = in_department

        with Session() as session:
            with session.begin():
                try:
                    result = session.query(cls).filter_by(**query).one()
                except Exception as E:
                    raise HourlyException('err.hourly.' + table_name + 'NotFound')

                return result


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

    children = relationship("Clockin")
    department = relationship("Department", back_populates="children")
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


# A Department is a section of employees that serves a particular purpose.
# Departments contain an ID, a name, and a respective description
class Department(HourlyTable, Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(255))
    manager_id = Column(Integer)
    company_id = Column(Integer(), ForeignKey('companies.id'), default=1)

    children = relationship('Employee')

    # Retrieves the budget for the department, if one exists.
    def get_budget(self):
        try:
            {'budget': self.budget.as_dict()}
        except:
            return {'budget': 'None'}

    # Represents a Department in dictionary form.
    def as_dict(self):
        return {
            "id": self.id,
            "department_name": self.department_name,
            "manager_id": self.manager_id,
            "company_id": self.company_id
        }


class Company(HourlyTable, Base):
    """ Represents a grouping of employees and services. Each company
        contains a bit of metadata about the company. A linking is
        maintained between the following fields and a company:
            -Departments
            -Employees
            -Packages
            -Clock-ins (linked by a department)
        by way of a foreign key.
    """

    __tablename__ = "companies"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    about = Column(String(255), nullable=False)
    address_street = Column(String(255), default="")
    city = Column(String(255), default="")
    state = Column(String(255), default="")
    zip_code = Column(String(255), default="")
    phone = Column(String(255), default="")

    def as_dict(self):
        """Represents this entity in dictionary form.

        :return: A dictionary with all fields of this model.
        :rtype dict
        """

        return {
            'id': self.id,
            "name": self.name,
            "about": self.about,
            "address_street": self.address_street,
            "city": self.city,
            "state": self.state,
            "zip_code": self.zip_code,
            "phone": self.phone
        }


"""
    Represents a unique privilege that identifies the capabilities of a user
    within the application. Includes a set of privileges to be validated against
    each request.
"""


class Roles(HourlyTable, Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    permissions = Column(Text())

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "permissions": self.permissions
        }

    def __repr__(self):
        return "<Role(name='%s'" % (
            self.name
        )


# A clockin is a transaction performed by an employee. Various
# clock-ins are associated with an employee by
class Clockin(HourlyTable, Base):
    __tablename__ = "clockins"

    # A one-to-many relationship is defined in which the
    # employee id in this table is a foreign key provided
    # in the employees table.
    id = Column(Integer(), primary_key=True, autoincrement=True)
    employee_id = Column(Integer(), ForeignKey('employees.id'))
    clockin_time = Column(DateTime(), server_default=func.now())
    clockout_time = Column(DateTime(), onupdate=func.now(), server_default=None)
    department_id = Column(Integer(), ForeignKey('departments.id'))
    parent = relationship("Employee", back_populates="children")
    department = relationship("Department")

    # Returns a dictionary representation of the Clockin.
    def as_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.parent.name,
            'clockin_time': self.clockin_time,
            'clockout_time': self.clockout_time,
            'department': self.department.as_dict()
        }


# A clockin is a transaction performed by an employee. Various
# clock-ins are associated with an employee by
class Package(HourlyTable, Base):
    __tablename__ = "packages"

    # A one-to-many relationship is defined in which the
    # employee id in this table is a foreign key provided
    # in the employees table.
    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False)
    description = Column(String(255))
    img_url = Column(String(255), default="")
    price = Column(Float, default=0.0)
    company_id = Column(Integer(), ForeignKey('companies.id'), nullable=False)
    questions = Column(JSON(), nullable=False)


class Event(HourlyTable, Base):
    """Represents a unique serviceable event within the system. Each
       event is an instantiation of a package, which can be serviced
       by a department within a company.

    """

    __tablename__ = "events"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String(255), nullable=False, default="")
    description = Column(String(255), default="")
    agreed_price = Column(Float, default=0.0)
    start_datetime = Column(DateTime(), nullable=False)
    end_datetime = Column(DateTime(), nullable=False)
    package_id = Column(Integer(), ForeignKey('packages.id'), nullable=False)
    company_id = Column(Integer(), ForeignKey('companies.id'), nullable=False)
    employee_id = Column(Integer(), ForeignKey('employees.id'))
    questions = Column(JSON(), nullable=False, default=[])


# If a table does not yet exist, create one on the database with
# the schema provided by Declarative relational mapping in SQLAlchemy.
Base.metadata.create_all(engine)

# By default, at least one company and one department must exist. Create if
# not already done so.
# get_or_create(Session, Company, id=1, name="Hourly", about="")
# get_or_create(Session, Department, department_name="Default Department", company_id=1)
