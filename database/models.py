import json
import re

import bcrypt
from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, Float, text, JSON, Boolean
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
    def query_table(cls, page=None, offset=None, limit=None, sort=None, include_totals=None, **kwargs) -> list:
        """Queries this table with specified parameters as designated in the request.

        :param page: Represents the page, calculated by the offset and, if any, a limit
        :param offset: Represents the offset from the first row in the table to query.
        :param limit: Represents the maximum number of records returned.
        :param sort: Represents a field to sort by, denoted as a ^ for asc or - for desc
        :param include_totals: Represents whether to include totals in the response
        :param kwargs: Represents the filters to be specified to query by.
        :return: Either a list of records or a tuple containing the records and totals, if specified.
        :rtype List or Tuple
        """
        with Session() as session:
            with session.begin():
                resultant_rows = session.query(cls)
                count = None
                if kwargs is not None:
                    resultant_rows = resultant_rows.filter_by(**kwargs)
                if include_totals is not None:
                    count = resultant_rows.count()
                if sort is not None:
                    sorting_criteria = {
                        "^": "asc",
                        "-": "desc",
                    }
                    resultant_rows = resultant_rows.order_by(text(sort[1:] + " " + sorting_criteria[sort[0]]))
                if limit is not None:
                    limit = int(limit)
                    if limit > MAX_LIMIT:
                        limit = MAX_LIMIT
                if page is not None:
                    page = int(page)
                    rows_per_page = limit if limit is not None else DEFAULT_LIMIT
                    resultant_rows = resultant_rows.offset(rows_per_page * page)
                    resultant_rows = resultant_rows.limit(rows_per_page)
                if page is None and (offset is not None or limit is not None):
                    if offset is not None:
                        resultant_rows = resultant_rows.offset(int(offset) or 0)
                    if limit is not None:
                        resultant_rows = resultant_rows.limit(limit or 0)
                iterator = map(lambda res: res.as_dict(), resultant_rows.all())
                return list(iterator), count

    @classmethod
    def add_row(cls, row: dict):
        """Adds a row to the designated HourlyTable.

            :param self:
            :param row: Represents the generic row to add to the database.
            :return: None
            """
        with Session() as session:
            with session.begin():
                impending_row = cls(**row)
                session.add(impending_row)

    @classmethod
    def patch_row(cls, patch_document_list: list):
        """Accepts a patch document and processes an update to a
           specific resource.

        :param patch_document_list: Represents a list of RFC patch documents.
        :type List[Any]
        :return: None
        """
        raise Exception('Operation unsupported.')

    @classmethod
    def __process_patch_document(cls, patch_document_list, index=0):
        """Processes a patch document operation on a specified
        document.

        :param patch_document_list: Represents the list of RFC-6902 patch
        docs.
        :param index: Represents the current index.
        :return: None
        """
        raise Exception('Operation unsupported.')

    @classmethod
    def delete_row(cls, uid: int):
        """Deletes the specified row by ID.

        :param uid: The id to delete by.
        :return: None
        """
        with Session() as session:
            with session.begin():
                result = session.query(cls).filter_by(id=uid)
                result.delete()

    @classmethod
    def validate_model(cls, row: dict) -> bool:
        """ Validates a dict model against the property set of its
            intended model.

        :param row: The dict to validate.
        :return: True, if all keys in the row are a subset of this model's keys.
        :rtype bool
        """
        result = True

        # Short circuit if there are no keys to be processed.
        if not row.keys():
            return False

        # Validate the impending row to be added is a subset of the model.
        if not row.keys() <= cls.__dict__.keys():
            result = False

        return result


# Represents an employee.
# TODO: Implement passlib SHA-256 encryption in constructor.
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
        profile["company"] = self.company.as_dict()
        profile["role"] = self.role.as_dict()
        return profile

    @classmethod
    def validate_employee_exists(cls, employee_id, in_company=None):
        """Validates that the employee exists. If this condition
        is False, raises an error that corresponds to this model.

        :param in_department: Represents the department to cross reference.
        :param in_company: Represents the company to cross reference.
        :param employee_id: Represents the id of the employee.
        :return: A Bool representing whether the row exists.
        """
        if in_company is not None:
            result, count = cls.query_table(id=employee_id, company_id=in_company)
        else:
            result, count = cls.query_table(id=employee_id)

        if len(result) == 0:
            raise HourlyException('err.hourly.UserNotFound')

        return result

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
        return "<User(email='%s', password='%s', name='%s', role_id='%s', covid_status='%s' department='%s'" % (
            self.email, self.password, self.name, self.role_id, self.covid_status, self.department_id
        )

    @classmethod
    def get_users_profile(cls, user_id):
        """Retrieves the user's profile by obtaining details regarding
        their respective department, company and role.

        :param user_id: The ID of the user to fetch the profile of.
        :return: A profile dict of the user's profile.
        """
        with Session() as session:
            with session.begin():
                result = session.query(cls).filter_by(id=user_id).one()
                if result is None:
                    return []
                else:
                    return [result.profile_dict()]


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

    @classmethod
    def validate_department_exists(cls, department_id, in_company=None):
        """Validates that the employee exists. If this condition
        is False, raises an error that corresponds to this model.

        :param department_id: Represents the id of the department.
        :param in_company: Represents a company to check the department within.
        :return: A Bool representing whether the row exists.
        """
        if in_company is not None:
            result, count = cls.query_table(id=department_id, company_id=in_company)
        else:
            result, count = cls.query_table(id=department_id)

        if len(result) == 0:
            raise HourlyException('err.hourly.DepartmentNotFound')

        return result


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
    name = Column(String(255))
    about = Column(String(255))
    address_street = Column(String(255))
    city = Column(String(255))
    state = Column(String(255))
    zip_code = Column(String(255))
    phone = Column(String(255))

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

    @classmethod
    def validate_company_exists(cls, company_id):
        """Validates that the employee exists. If this condition
        is False, raises an error that corresponds to this model.

        :param company_id: Represents the company id.
        :return: A Bool representing whether the row exists.
        """
        result, count = cls.query_table(id=company_id)

        if len(result) == 0:
            raise HourlyException('err.hourly.CompanyNotFound')

        return result


"""
    Represents a unique privilege that identifies the capabilities of a user
    within the application. Includes a set of privileges to be validated against
    each request.
"""


class Roles(HourlyTable, Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))
    permissions = Column(String(255))

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "permissions": self.permissions
        }

    def validate_role_exists(cls, role_id):
        """Validates that the employee exists. If this condition
        is False, raises an error that corresponds to this model.

        :param employee_id: Represents the id of the employee.
        :return: A Bool representing whether the row exists.
        """
        result, count = cls.query_table(id=role_id)

        if len(result) == 0:
            raise HourlyException('err.hourly.RoleNotFound')

        return result

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

    @classmethod
    def validate_clockin_exists(cls, clockin_id):
        """Validates that the employee exists. If this condition
        is False, raises an error that corresponds to this model.

        :param clockin_id: The clockin ID.
        :return: A Bool representing whether the row exists.
        """
        result, count = cls.query_table(employee_id=clockin_id)

        if len(result) == 0:
            raise HourlyException('err.hourly.ClockinNotFound')

        return result


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
    img_url = Column(String(255))
    price = Column(Float, default=0.0)
    company_id = Column(Integer(), ForeignKey('companies.id'), nullable=False)
    questions = Column(JSON(), nullable=False)

    # Returns a dictionary representation of the Package.
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'img_url': self.img_url,
            'price': self.price,
            'questions': self.questions
        }

    @classmethod
    def validate_package_questions(cls, question_list):
        """Validates a list of package question. Any element
        within the package question list that does not meet the criteria
        is removed.

        :param question_list: Represents the list of questions being validated.
        :return: None
        """
        if not isinstance(question_list, list):
            return
        for i in range(0, len(question_list)):
            if not all(x in ['title', 'value', 'values', 'dataType'] for x in question_list[i]):
                question_list.remove(question_list[i])
        return question_list

    @classmethod
    def validate_package_exists(cls, package_id, in_company=None):
        """Validates that the employee exists. If this condition
        is False, raises an error that corresponds to this model.

        :param in_company: Represents the company to cross reference.
        :param package_id: Represents the id of the package.
        :return: A Bool representing whether the row exists.
        """
        filters = {id: package_id}
        if in_company is not None:
            result, count = cls.query_table(id=package_id, company_id=in_company)
        else:
            result, count = cls.query_table(id=package_id)

        if len(result) == 0:
            raise HourlyException('err.hourly.PackageNotFound')

        return result


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
    end_datetime = Column(DateTime())
    package_id = Column(Integer(), ForeignKey('packages.id'), nullable=False)
    service_employee = Column(Integer(), ForeignKey('employees.id'), default=None)
    department_id = Column(Integer(), ForeignKey('departments.id'), nullable=False)

    def as_dict(self):
        """Returns a dictionary representation of the Event.

        :return: A dictionary representation of the Event.
        """
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "agreed_price": self.agreed_price,
            "start_datetime": self.start_datetime,
            "end_datetime": self.end_datetime,
            "package_id": self.package_id,
            "service_employee": self.service_employee,
            "department_id": self.department_id
        }

    @classmethod
    def validate_event_exists(cls: 'Event', event_id: int):
        """Validates that the event exists. If this condition
        is False, raises an error that corresponds to this model.

        :param event_id: The event id.
        :type event_id: int
        :return: A Bool representing whether the row exists.
        """
        result, count = cls.query_table(id=event_id)

        if len(result) == 0:
            raise HourlyException('err.hourly.EventNotFound')

        return result


# If a table does not yet exist, create one on the database with
# the schema provided by Declarative relational mapping in SQLAlchemy.
Base.metadata.create_all(engine)

# By default, at least one company and one department must exist. Create if
# not already done so.
get_or_create(Session, Company, id=1, name="Hourly")
get_or_create(Session, Department, department_name="Default Department", company_id=1)
