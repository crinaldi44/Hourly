from marshmallow import fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from database.database import Base
from database.base import HourlyTable
from database.company import validate_company


class Department(HourlyTable, Base):
    __tablename__ = "departments"
    id = Column(Integer, primary_key=True, autoincrement=True)
    department_name = Column(String(255))
    manager_id = Column(Integer)
    company_id = Column(Integer(), ForeignKey('companies.id'), default=1)

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


class DepartmentModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        load_instance = True
        include_fk = True

    company_id = fields.Integer(validate=validate_company)


def validate_department(department_id):
    return Department.validate_exists(id=department_id, table_name="Department")