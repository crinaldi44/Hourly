from marshmallow import Schema, fields, INCLUDE, validate
from marshmallow.validate import Length
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, SQLAlchemySchema

from database.models import Clockin, Company, Department, Employee, Event, Package, Roles


def validate_department(department_id):
    return Department.validate_exists(id=department_id, table_name="Department")


def validate_company(company_id):
    return Company.validate_exists(id=company_id, table_name="Company")


def validate_employee(employee_id):
    return Employee.validate_exists(id=employee_id)


class PatchDocumentModel(Schema):
    """Represents an RFC-6902 compliant JSON Patch Document. Fields
    are included for the operation being performed, the path, and the
    impending value.

    """
    op = fields.String(required=True, validate=validate.OneOf(['add', 'remove', 'replace']))
    path = fields.String()
    value = fields.Raw()


class PackageQuestionModel(Schema):
    """Represents a listing of questions to be included within a
    Package or an Event.

    """
    title = fields.String(required=True)
    data_type = fields.String(required=True)
    # values = fields.List(cls_or_instance=)


class QueryFilter(Schema):
    """Represents a query filter object that will test that the specified filters
    meet expectations.

    """
    filters = fields.Dict(validate=validate.NoneOf(['company_id', 'id']))
    page = fields.Integer()
    offset = fields.Integer()
    limit = fields.Integer(validate=validate.Range(min=0, max=100))
    sort = fields.Str()
    include_totals = fields.Str()


class ClockinModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Clockin
        load_instance = True
        include_fk = True


class CompanyModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Company
        load_instance = True
        include_fk = True

    name = fields.Str(required=True, validate=Length(min=3, max=50))


class DepartmentModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Department
        load_instance = True
        include_fk = True

    company_id = fields.Integer(validate=validate_company)


class EmployeeModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Employee
        load_instance = True
        include_fk = True

    email = fields.Email()
    password = fields.Str(validate=Length(min=8, max=100), load_only=True,
                          error_messages={"length": "Length of field 'password' must be between 8 and 100 characters."})
    first_name = fields.Str(required=True, error_messages={"required": "Field 'first_name' is required!"})
    last_name = fields.Str(required=True)
    pay_rate = fields.Float(required=True, validate=validate.Range(min=0.00),
                            error_messages={"range": "Field 'pay_rate' must be a non-negative number."})
    title = fields.Str(validate=Length(max=50))
    department_id = fields.Integer(required=True, validate=validate_department,
                                   error_messages={"required": "Field 'department_id' is required for type Employee."})
    company_id = fields.Integer(validate=validate_company)


class EventModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Event
        load_instance = True
        include_fk = True

    company_id = fields.Integer(required=True, validate=validate_company)
    assigned_employee = fields.Integer(validate=validate_employee)


class PackageModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Package
        load_instance = True
        include_fk = True

    price = fields.Float(min=0.0, allow_nan=False, allow_none=False, as_string=False)


class RoleModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
        load_instance = True
        include_fk = True
