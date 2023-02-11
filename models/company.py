from marshmallow import fields
from marshmallow.validate import Length
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Integer, String

from crosscutting.core.db.database import Base
from models.base import HourlyTable


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


class CompanyModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = True
        include_fk = True

    name = fields.Str(required=True, validate=Length(min=3, max=50))


def validate_company(company_id):
    return Company.validate_exists(id=company_id, table_name="Company")