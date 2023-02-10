from marshmallow import Schema, fields
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey, JSON

from crosscutting.db.database import Base
from models.base import HourlyTable
from models.package import PackageQuestionModel


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
    invoice_items = Column(JSON(), default=[])


class EventSearch(Schema):
    """Represents a event query filter object that will test that the specified filters
    meet expectations.

    """
    from_date = fields.DateTime(required=True)
    to_date = fields.DateTime(required=True)
    package_name = fields.Str()


class InvoiceItemModel(Schema):
    """Represents a set of data containing the invoice item data.

    """
    name = fields.String(required=True)
    price = fields.List(fields.Float(required=True, default=0.0))


class EventModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        load_instance = True
        include_fk = True

    description = fields.Str()
    agreed_price = fields.Float()
    company_id = fields.Integer(required=False, dump_only=True)  # This should be read only, as it is set on add.
    employee_id = fields.Integer()
    package_id = fields.Integer(required=True)
    start_datetime = fields.DateTime(required=True)
    end_datetime = fields.DateTime(required=True)
    questions = fields.List(fields.Nested(PackageQuestionModel))
    invoice_items = fields.List(fields.Nested(InvoiceItemModel))
