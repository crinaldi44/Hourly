from inflection import underscore, camelize
from marshmallow import pre_load, post_dump, Schema, fields, validate

from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.core.db.database import Session

"""Represents the default number of rows per page for a user
   response.
"""
DEFAULT_LIMIT = 20

MAX_LIMIT = 100


class HourlyTable(object):
    """Represents a class whose primary function is to serve data to the user.
       The class is intended to be an extension of the Base to provide static
       functionality to the table objects.
    """

    @classmethod
    def validate_exists(cls, id, in_company=None, in_department=None, table_name="Company"):
        """Validates that the employee exists. If this condition
        is False, raises an error that corresponds to this model.

        :param table_name:
        :param in_department:
        :param id: Represents the id of the resource.
        :param in_company: Represents a company to check the resource within.
        :return: A Bool representing whether the row exists.
        """
        query = {
            "id": id
        }
        if in_company is not None:
            query["company_id"] = in_company
        if in_department is not None:
            query["department_id"] = in_department

        with Session() as session:
            with session.begin():
                try:
                    result = session.query(cls).filter_by(**query).one()
                except Exception as E:
                    raise HourlyException('err.hourly.' + table_name + 'NotFound')

                return result


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
