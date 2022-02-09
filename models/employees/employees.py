from sqlalchemy import Column, Integer, String, ForeignKey, func, DateTime, Float
from sqlalchemy.orm import declarative_base, relationship
from models.database import engine, Base


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
    department_id = Column(Integer(), ForeignKey('departments.id'))
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
            'department_id': self.department_id,
            'covid_status': self.covid_status
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
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(255))
    manager_id = Column(Integer)
    children = relationship('Employee')

    # Represents a Department in dictionary form.
    def as_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "manager_id": self.manager_id
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
    parent = relationship("Employee", back_populates="children")

    # Returns a dictionary representation of the Clockin.
    def as_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'clockin_time': self.clockin_time,
            'clockout_time': self.clockout_time,
        }


# If a table does not yet exist, create one on the database with
# the schema provided by Declarative relational mapping in SQLAlchemy.
Base.metadata.create_all(engine)
