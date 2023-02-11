from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Integer, String, Text

from crosscutting.core.db.database import Base
from models.base import HourlyTable


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


class RoleModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
        load_instance = True
        include_fk = True