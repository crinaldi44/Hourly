import ast

from jsonpatch import JsonPatch, JsonPatchException
from marshmallow import Schema
from sqlalchemy import text
from sqlalchemy.orm import load_only

from crosscutting.exception.hourly_exception import HourlyException
from crosscutting.core.db.database import Session

DEFAULT_LIMIT = 20
MAX_LIMIT = 100

PROTECTED_FIELDS = [
    'id',
    'company_id',
    'role_id'
]


class Service:
    """
    The Service (schema) layer of a domain is generally designed to handle interaction
    with the Data Access Layer (the model). Classes of this type provide functionality
    to manipulate and interact with data.

    Generally, wherever possible, to cut down on the number of sessions open with the
    Database, you'll want to prioritize or create methods that make use of a single session
    versus sequentially invoking methods that would lead to multiple sessions being created.

    """

    def __init__(self, model, openapi_type, table_name="None"):
        """Initializes a new Service.

        :param model: Represents the DAO this Service will interact with.
        :type schema: Schema
        """
        self.table_name = table_name
        self.name = table_name.capitalize()
        self.openapi_type = openapi_type
        self.model = model

    @classmethod
    def sanitize_q(cls, q_str):
        """Sanitizes a q object to filter out restricted keys
        such that a user cannot filter by prohibited fields.

        :param q_str: Represents the raw q string.
        :return: A modified q string without the restricted keys.
        """
        reduction = ast.literal_eval(q_str)
        return {k: v for (k, v) in reduction.items() if not any(x in ['company_id', 'department_id', 'id'] for x in k)}

    def sanitize_patch_document(self, patch_document_list, index=0):
        """Sanitizes a patch document by traversing through until it
        finds a potential path that is prohibited for edit.

        :param patch_document_list:
        :param index:
        :return:
        """
        if index >= len(patch_document_list):
            return
        document = patch_document_list[index]
        if any(x in document['path'] for x in PROTECTED_FIELDS):
            raise HourlyException('err.hourly.InvalidPatch')
        else:
            self.sanitize_patch_document(patch_document_list, index + 1)

    def _process_fields(self, fields):
        """
        Parses the fields field.

        :param fields:
        :return:
        """
        new_fields = ast.literal_eval(fields)
        return new_fields

    def list_rows(self, q=None, offset=None, limit=None, sort=None, include_totals=True, fields=None,
                  additional_filters=None):
        """
        Lists the rows matching the specified query. Converts to dict and constructs the rows to the
        OpenAPI type for use with controllers.

        :param additional_filters: Represents the additional filters applied after the q by the API.
        :param q: Represents the query object.
        :param page: Represents the page, calculated by the offset and, if any, a limit
        :param offset: Represents the offset from the first row in the table to query.
        :param limit: Represents the maximum number of records returned.
        :param sort: Represents a field to sort by, denoted as a ^ for asc or - for desc

        :return: Either a list of records or a tuple containing the records and totals, if specified.
        :rtype List or Tuple
        """
        with Session() as session:
            with session.begin():
                resultant_rows = session.query(self.model)
                if q is not None:
                    resultant_rows = resultant_rows.filter_by(**ast.literal_eval(q))
                if additional_filters is not None:
                    resultant_rows = resultant_rows.filter_by(**additional_filters)
                count = resultant_rows.count()
                try:
                    if sort is not None:
                        sorting_criteria = {
                            "^": "asc",
                            "-": "desc",
                        }
                        resultant_rows = resultant_rows.order_by(text(sort[1:] + " " + sorting_criteria[sort[0]]))
                    if limit is not None:
                        limit = int(limit)
                        if limit > MAX_LIMIT:
                            limit = MAX_LIMIT
                        resultant_rows.limit(limit)
                    if offset is not None:
                        resultant_rows = resultant_rows.offset(offset)
                    if fields is not None:
                        resultant_rows = resultant_rows.options(load_only(*self._process_fields(fields)))
                except:
                    raise HourlyException("err.hourly.InvalidQuery")
                rows = list(map(lambda x: self._to_openapi_type(x), resultant_rows.all()))
                return rows, count

    def validate_exists(self, filters=None):
        """
        Queries to find the first element that matches the specified search query. If none
        is found, raises an exception to the user.

        :param filters:
        :return:
        """
        with Session() as session:
            with session.begin():
                try:
                    result = session.query(self.model).filter_by(**filters).one()
                    return self._to_openapi_type(result)
                except:
                    raise HourlyException('err.hourly.' + self.name + 'NotFound')

    def _to_openapi_type(self, model):
        """
        Converts a SQLAlchemy model dict to an OpenAPI type.
        """
        return self.openapi_type(**model.to_dict())

    def from_json(self, data):
        """Validates the specified model. If an invalid value has been encountered,
        raises an exception which will call back to the user with the fields that
        are invalid. Deserializes the model into a models model.

        :param data:
        :param dikt:
        :return: A dikt instance of the model
        """
        return self.openapi_type(**data)

    def patch(self, uid: int, patch_list: list):
        """Patches the specified resource using RFC-6902 compliant patch documents.
        Resolves JSON pointers in the patch list to fields in the document. Processes
        operations in order.

        :param uid: Represents the ID of the resource to patch.
        :param patch_list: Represents a listing of patch documents.
        :return: The patched resource
        """
        if len(patch_list) == 0:
            return
        patch = JsonPatch(patch_list)
        self.sanitize_patch_document(patch_list)

        with Session() as session:
            # Keep transactions in same context to avoid issues with model expiration.
            with session.begin():
                result = session.query(self.model).filter_by(id=uid)
                records = result.all()
                if len(records) == 0:
                    raise HourlyException('err.hourly.' + self.name + 'NotFound')
                try:
                    # Dump existing model, apply the replacement doc with validations
                    # and update to new row.
                    diff_doc = patch.apply(records[0].to_dict())
                    self.from_json(diff_doc)  # Validate the model.
                    result.update(diff_doc)
                except JsonPatchException as E:
                    raise HourlyException('err.hourly.InvalidPatch')

    def add_row(self, row):
        """
        Adds the row to the target table. Attempts to validate the row prior to entry to ensure compliance
        with the desired schema, then inserts.

        :param row: Represents the row to add.
        :return: None
        """
        with Session() as session:
            with session.begin():
                try:
                    session.add(self.model(**row.to_dict()))
                except ValueError as E:
                    raise HourlyException(f"err.hourly.Bad{self.name}Formatting", message=E.__str__())

    def delete_row(self, row_id: int):
        """Deletes the specified row by ID.

        :param row_id: The id to delete by.
        :return: None
        """
        with Session() as session:
            with session.begin():
                result = session.query(self.model).filter_by(id=row_id)
                if result is None:
                    raise HourlyException(f"err.hourly.{self.name}NotFound")
                result.delete()
