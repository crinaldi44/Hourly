from marshmallow import Schema, fields, INCLUDE, validate, pre_load, post_dump
from marshmallow.validate import Length
from marshmallow_sqlalchemy import SQLAlchemyAutoSchema, auto_field, SQLAlchemySchema

from database.models import Clockin, Company, Department, Employee, Event, Package, Roles
from inflection import underscore, camelize


def validate_department(department_id):
    return Department.validate_exists(id=department_id, table_name="Department")


def validate_package(package_id):
    return Package.validate_exists(id=package_id, table_name="Package")


def validate_company(company_id):
    return Company.validate_exists(id=company_id, table_name="Company")


def validate_employee(employee_id):
    return Employee.validate_exists(id=employee_id)


class FormatConverter:
    """This mixin ensures uniform formatting for the user request data coming in
    as well as going out, specifically that all data that is returned to the user
    is converted to camelCased and all data coming in is snake cased.

    """

    @pre_load
    def to_snakecase(self, data, **kwargs):
        return {underscore(key): value for key, value in data.items()}

    @post_dump
    def to_camelcase(self, data, **kwargs):
        return {camelize(key, uppercase_first_letter=False): value for key, value in data.items()}


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
    data_type = fields.String(required=True,
                              validate=validate.OneOf(['multiselect', 'dropdown', 'textfield', 'paragraph']))
    value = fields.String(default="")
    values = fields.List(fields.Str())


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

    description = fields.Str()
    agreed_price = fields.Float()
    company_id = fields.Integer(required=False, dump_only=True)  # This should be read only, as it is set on add.
    employee_id = fields.Integer()
    package_id = fields.Integer(required=True)
    start_datetime = fields.DateTime(required=True)
    end_datetime = fields.DateTime(required=True)
    questions = fields.List(fields.Nested(PackageQuestionModel))


class PackageModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Package
        load_instance = True
        include_fk = True

    price = fields.Float(min=0.0, allow_nan=False, allow_none=False, as_string=False)
    questions = fields.List(fields.Nested(PackageQuestionModel))


class RoleModel(SQLAlchemyAutoSchema):
    class Meta:
        model = Roles
        load_instance = True
        include_fk = True
