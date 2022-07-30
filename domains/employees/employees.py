from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, Float, text, Boolean
from sqlalchemy.orm import relationship
from database.database import engine, Base, Session
from domains.employees.utils.utils import get_or_create


class HourlyTable(object):
    """Represents a class whose primary function is to serve data to the user.
       The class is intended to be an extension of the Base to provide static
       functionality to the table objects.
    """

    """Represents the default number of rows per page for a user
       response.
    """
    DEFAULT_LIMIT = 20

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
                if page is not None:
                    page = int(page)
                    rows_per_page = int(limit) if limit else DEFAULT_LIMIT
                    resultant_rows = resultant_rows.offset(rows_per_page * page)
                    resultant_rows = resultant_rows.limit(rows_per_page)
                if page is None and (offset is not None or limit is not None):
                    resultant_rows = resultant_rows.offset(int(offset) or 0)
                    resultant_rows = resultant_rows.limit(int(limit) or 0)
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
    email = Column(String(255))
    password = Column(String(255))
    name = Column(String(255))
    pay_rate = Column(Float)
    title = Column(String(255))
    department_id = Column(Integer(), ForeignKey('departments.id'))
    role_id = Column(Integer(), ForeignKey('roles.id'))
    company_id = Column(Integer(), ForeignKey('companies.id'), default=1)
    account_disabled = Column(Boolean(), default=False)

    children = relationship("Clockin")
    parent = relationship("Department", back_populates="children")
    company = relationship("Company")
    role = relationship("Roles")

    # Represents the Employee as a dictionary, for serialization in JSON
    # response.
    def as_dict(self):
        return {
            'id': self.id,
            'password': self.password,
            'email': self.email,
            'name': self.name,
            'pay_rate': self.pay_rate,
            'title': self.title,
            "role_id": self.role_id,
            "company_id": self.company_id,
            'department': self.parent.as_dict(),
        }

    def profile_dict(self):
        """Represents this entity with additional profile information.

        :return: The profile, with additional company and role information.
        :rtype dict
        """
        profile = self.as_dict()
        profile["company_id"] = self.company.as_dict()
        profile["role_id"] = self.role.as_dict()
        return profile

    # Represents a machine-readable representation of the state of the
    # Employee.
    def __repr__(self):
        return "<User(email='%s', password='%s', name='%s', role_id='%s', covid_status='%s' department='%s'" % (
            self.email, self.password, self.name, self.role_id, self.covid_status, self.department_id
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
            "manager_id": self.manager_id
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


"""
    Represents a unique privilege that identifies the capabilities of a user
    within the application. Includes a set of privileges to be validated against
    each request.
"""


class Roles(HourlyTable, Base):
    __tablename__ = "roles"
    id = Column(Integer, primary_key=True)
    name = Column(String(255))

    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name
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
    name = Column(String(255))
    description = Column(String(255))
    img_url = Column(String(255))
    price = Column(Float, default=0.0)
    company_id = Column(Integer(), ForeignKey('companies.id'))

    # Returns a dictionary representation of the Clockin.
    def as_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'description': self.description,
            'img_url': self.img_url,
            'price': self.price
        }


class Event(HourlyTable, Base):
    """Represents a unique serviceable event within the system. Each
       event is an instantiation of a package, which can be serviced
       by a department within a company.

    """

    __tablename__ = "events"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    description = Column(String(255))
    agreed_price = Column(Float, default=0.0)
    start_datetime = Column(DateTime())
    end_datetime = Column(DateTime())
    package_id = Column(Integer(), ForeignKey('packages.id'))
    service_employee = Column(Integer(), ForeignKey('employees.id'), default=None)
    department_id = Column(Integer(), ForeignKey('departments.id'))



# If a table does not yet exist, create one on the database with
# the schema provided by Declarative relational mapping in SQLAlchemy.
Base.metadata.create_all(engine)

# By default, at least one company and one department must exist. Create if
# not already done so.
get_or_create(Session, Company, id=1, name="Hourly")
get_or_create(Session, Department, department_name="Default Department", company_id=1)
