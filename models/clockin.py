from marshmallow_sqlalchemy import SQLAlchemyAutoSchema
from sqlalchemy import Column, Integer, ForeignKey, DateTime, func

from crosscutting.core.db.database import Base
from models.base import HourlyTable


class Clockin(HourlyTable, Base):
    __tablename__ = "clockins"

    id = Column(Integer(), primary_key=True, autoincrement=True)
    employee_id = Column(Integer(), ForeignKey('employees.id'))
    clockin_time = Column(DateTime(), server_default=func.now())
    clockout_time = Column(DateTime(), onupdate=func.now(), server_default=None)
    department_id = Column(Integer(), ForeignKey('departments.id'))

    def as_dict(self):
        return {
            'id': self.id,
            'employee_id': self.employee_id,
            'employee_name': self.parent.name,
            'clockin_time': self.clockin_time,
            'clockout_time': self.clockout_time,
            'department': self.department.as_dict()
        }


class ClockinModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Clockin
        load_instance = True
        include_fk = True
