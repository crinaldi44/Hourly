import ast
from typing import Tuple, List, Any

from jsonpatch import JsonPatch, JsonPatchException
from marshmallow import Schema
from sqlalchemy import text

from crosscutting.exception.hourly_exception import HourlyException
from database.database import Session

DEFAULT_LIMIT = 20
MAX_LIMIT = 100

PROTECTED_FIELDS = [
    'id',
    'company_id',
    'role_id'
]


class Service:
    """The Service (schema) layer of a domain is generally designed to handle interaction
    with the Data Access Layer (the model). Classes of this type provide functionality
    to manipulate and interact with data.

    Generally, wherever possible, to cut down on the number of sessions open with the
    Database, you'll want to prioritize or create methods that make use of a single session
    versus sequentially invoking methods that would lead to multiple sessions being created.

    """

    def __init__(self, model, schema: Schema, table_name="None"):
        """Initializes a new Service.

        :param model: Represents the Data Access Object this Service will interact with.
        :type model: Base
        :param schema: Represents the Schema this Service will interact with.
        :type schema: Schema
        """
        self.table_name = table_name
        self.name = table_name.capitalize()
        self.model = model
        self.schema = schema()

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

    def find(self, q=None, page=None, offset=None, limit=None, sort=None, include_totals=None, serialize=False,
             additional_filters=None):
        """Queries this table with specified parameters as designated in the request.

        :param additional_filters: Represents the additional filters applied after the q by the API.
        :param q: Represents the query object.
        :param serialize: Represents whether to serialize results.
        :param page: Represents the page, calculated by the offset and, if any, a limit
        :param offset: Represents the offset from the first row in the table to query.
        :param limit: Represents the maximum number of records returned.
        :param sort: Represents a field to sort by, denoted as a ^ for asc or - for desc
        :param include_totals: Represents whether to include totals in the response
        :param kwargs: Represents the filters to be specified to query by.
        :return: Either a list of records or a tuple containing the records and totals, if specified.
        :rtype List or Tuple
        """
        with Session(expire_on_commit=False) as session:
            with session.begin():
                resultant_rows = session.query(self.model)
                count = None
                if q is not None:
                    resultant_rows = resultant_rows.filter_by(**ast.literal_eval(q))
                if additional_filters is not None:
                    resultant_rows = resultant_rows.filter_by(**additional_filters)
                if include_totals is not None:
                    count = resultant_rows.count()
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
                if page is not None:
                    page = int(page)
                    rows_per_page = limit if limit is not None else DEFAULT_LIMIT
                    resultant_rows = resultant_rows.offset(rows_per_page * page)
                    resultant_rows = resultant_rows.limit(rows_per_page)
                if page is None and (offset is not None or limit is not None):
                    if offset is not None:
                        resultant_rows = resultant_rows.offset(int(offset) or 0)
                    if limit is not None:
                        resultant_rows = resultant_rows.limit(limit or 0)
                if serialize is True:
                    iterator = map(lambda res: self.schema.dump(res), resultant_rows.all())
                    return list(iterator), count
                else:
                    return resultant_rows.all(), count

    def validate_exists(self, id: int, in_company: int = None, in_department: int = None):
        """Finds an entry within the database with the specified id. If
        fields for in_company or in_department or specified, the model must
        have a field called "company_id" or "department_id" respectively,
        otherwise this will not return a value.

        :param in_department: Represents the department to search within.
        :type in_department: int
        :param in_company: Represents the company to search within.
        :type in_company: int
        :param id: Represents the ID of the resource.
        :type id: int
        :return: A list containing the resource.
        """
        query = {
            "id": id
        }
        if in_company is not None:
            query["company_id"] = in_company
        if in_department is not None:
            query["department_id"] = in_department
        result, count = self.find(additional_filters=query, include_totals=True)
        if count == 0:
            raise HourlyException('err.hourly.' + self.name + 'NotFound')
        return result[0]

    def as_dict(self, model):
        """Serializes this model into dict format.

        :return: A dict representation of the model.
        """
        return self.schema.dump(model)

    def from_json(self, data):
        """Validates the specified model. If an invalid value has been encountered,
        raises an exception which will call back to the user with the fields that
        are invalid. Deserializes the model into a database model.

        :param data:
        :param dikt:
        :return: A dikt instance of the model
        """
        return self.schema.load(data=data, session=Session())

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
                    diff_doc = patch.apply(self.schema.dump(records[0]))
                    self.from_json(diff_doc) # Validate the model.
                    result.update(diff_doc)
                except JsonPatchException as E:
                    raise HourlyException('err.hourly.InvalidPatch')

    @classmethod
    def add_row(cls, row):
        """Adds a row to the table. Note that this does not deserialize or validate the model
        you are attempting to add. For the version that achieves both of these, you may use
        the Service.add_json() method. Otherwise, if you need to manipulate or utilize the
        impending data, simply call validate_model which will deserialize the model from JSON,
        then you may simply add the validated model using this method.

        :param row: Represents the row to add.
        :return: None
        """
        with Session() as session:
            with session.begin():
                session.add(row)

    def add_json(self, dikt: dict):
        """Adds a JSON serialized row to the specified table. Validates
        the JSON. This generally should be utilized when no further manipulation
        of user data is required and the document may be directly imported.

        :param dikt:
        :return:
        """
        with Session() as session:
            with session.begin():
                impending_row = self.schema.load(data=dikt, session=self.session)
                session.add(impending_row)

    def delete_row(self, uid: int):
        """Deletes the specified row by ID.

        :param uid: The id to delete by.
        :return: None
        """
        with Session() as session:
            with session.begin():
                result = session.query(self.model).filter_by(id=uid)
                result.delete()
