import json

from marshmallow import Schema, fields, validate, pre_load
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Integer, String, Float, ForeignKey, JSON

from crosscutting.core.db.database import Base
from models.base import HourlyTable


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


class PackageQuestionModel(Schema):
    """Represents a listing of questions to be included within a
    Package or an Event.

    """
    title = fields.String(required=True)
    data_type = fields.String(required=True,
                              validate=validate.OneOf(['multiselect', 'dropdown', 'textfield', 'paragraph']))
    value = fields.String(default="")
    values = fields.List(fields.Str())


class PackageModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Package
        load_instance = True
        include_fk = True

    price = fields.Float(min=0.0, allow_nan=False, allow_none=False, as_string=False)
    questions = fields.List(fields.Nested(PackageQuestionModel))

    @pre_load
    def parse_questions(self, data, **kwargs):
        if isinstance(data["questions"], str):
            data["questions"] = json.loads(data["questions"])
        return data


def validate_package(package_id):
    return Package.validate_exists(id=package_id, table_name="Package")