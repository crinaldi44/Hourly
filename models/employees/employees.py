from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship
from models.database import engine, Base, Session
from models.employees.utils import get_or_create


# Represents an employee.
# TODO: Implement passlib SHA-256 encryption in constructor.
class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True)

    password = Column(String(255))
    email = Column(String(255))
    name = Column(String(255))
    pay_rate = Column(Float)
    title = Column(String(255))
    department_id = Column(Integer(), ForeignKey('departments.department_id'))
    covid_status = Column(String(255))

    children = relationship("Clockin")
    parent = relationship("Department", back_populates="children")

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
            'covid_status': self.covid_status,
            'department': self.parent.as_dict(),
        }

    # Represents a machine-readable representation of the state of the
    # Employee.
    def __repr__(self):
        return "<User(email='%s', password='%s', name='%s', covid_status='%s' department='%s'" % (
            self.email, self.password, self.name, self.covid_status, self.department_id
        )


# A Department is a section of employees that serves a particular purpose.
# Departments contain an ID, a name, and a respective description
class Department(Base):
    __tablename__ = "departments"
    department_id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(255))
    manager_id = Column(Integer)
    budget_id = Column(Integer, ForeignKey('budget.budget_id'))
    budget = relationship('Budget')
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
            "department_id": self.department_id,
            "department_name": self.department_name,
            "manager_id": self.manager_id
        }

# A budget is a period of absolute maximum payroll amount for a
# specific department. A budget can contain a maximum dollar
# amount as well as a max dollar amount.
class Budget(Base):
    __tablename__ = "budget"
    budget_id = Column(Integer, primary_key=True, autoincrement=True)
    budget_hours = Column(Integer)
    budget_dollars = Column(Float)
    effective_date = Column(DateTime)
    date_deleted = Column(DateTime)

    # Represents a dictionary representation.
    def as_dict(self):
        return {
            "budget_id": self.budget_id,
            "budget_hours": self.budget_hours,
            "budget_dollars": self.budget_dollars,
            "effective_date": self.effective_date,
            "date_deleted": self.date_deleted
        }

# A clockin is a transaction performed by an employee. Various
# clock-ins are associated with an employee by
class Clockin(Base):
    __tablename__ = "clockins"

    # A one-to-many relationship is defined in which the
    # employee id in this table is a foreign key provided
    # in the employees table.
    id = Column(Integer(), primary_key=True, autoincrement=True)
    employee_id = Column(Integer(), ForeignKey('employees.id'))
    clockin_time = Column(DateTime(), server_default=func.now())
    clockout_time = Column(DateTime(), onupdate=func.now(), server_default=None)
    department_id = Column(Integer(), ForeignKey('departments.department_id'))
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


# If a table does not yet exist, create one on the database with
# the schema provided by Declarative relational mapping in SQLAlchemy.
Base.metadata.create_all(engine)

# By default, at least one 'primary'/'admin' department must exist
# by the name of management. Create if it does not exists.
get_or_create(Session, Department, department_name="Management")
