"""
    Contains general functionality to query a model, including processing a patch to a
    grouping of documents.
"""
from sqlalchemy import text

from database.database import Base, Session

# Represents the default limit on a dataset if paginated return
# values are requested.
DEFAULT_LIMIT = 20

"""
    Queries the given table based on the model using the provided
    filtering functionality. Utilizes an instance of the Session 
    contextually and iteratively converts the results to 
    dictionary format.
    
    Returns:
        A list of the respective rows in dictionary format.
"""


def query_table(model: Base, page=None, offset=None, limit=None, sort=None, include_totals=None, **kwargs) -> list:
    with Session() as session:
        with session.begin():
            resultant_rows = session.query(model)
            count = None
            if kwargs is not None:
                resultant_rows = resultant_rows.filter_by(**kwargs)
            if include_totals is not None:
                count = resultant_rows._total_count()
            if sort is not None:
                sorting_criteria = {
                    "^": "asc",
                    "-": "desc",
                }
                resultant_rows = resultant_rows.order_by(text(sort[1:] + " " + sorting_criteria[sort[0]]))
            if page is not None:
                page = int(page)
                rows_per_page = int(limit) if limit else DEFAULT_LIMIT
                resultant_rows = resultant_rows.offset(rows_per_page * page)
                resultant_rows = resultant_rows.limit(rows_per_page)
            if page is None and (offset is not None or limit is not None):
                resultant_rows = resultant_rows.offset(int(offset) or 0)
                resultant_rows = resultant_rows.limit(int(limit) or 0)
            iterator = map(lambda res: res.as_dict(), resultant_rows.all())
            return list(iterator), count


"""
    Adds the specified row into the selected model. It is recommended to
    validate the impending row against the model's keyset and provide any
    pre-processing to the respective fields prior to adding it using the
    validate_model helper function.
    
    Returns:
        void 
"""


def add_row(model: Base, row: dict):
    with Session() as session:
        with session.begin():
            impending_row = model(**row)
            session.add(impending_row)


"""
    Accepts a patch document list which is the list of fields and operations
    to be performed on the specified row within the model set.
    
    Returns:
        void
"""


def patch_row(model: Base, patch_list: list):
    raise Exception('Operation unsupported.')


"""
    Deletes the specified row by id or, optionally, by
    a designated field name.
    
    Returns:
        void
"""


def delete_row(model: Base, uid: int):
    with Session() as session:
        with session.begin():
            result = session.query(model).filter_by(id=uid)
            result.delete()


"""
    Replaces the specified row within the model. The new row takes the form of
    a dictionary and is validated accordingly prior to replacement. As a warning,
    this method automatically validates the impending row against the keyset of
    the model.
    
    Returns:
        void
"""
# def replace_row(model: Base, new_row: dict):
#     with Session() as session:
#         with session.begin():
#             if validate_model(model, new_row):
#                 ses
#             else:
#                 raise HourlyException('')


"""
    Validates the keys of a dictionary against the field requirements
    as defined in the model. Validates that the dictionary is of valid
    dict/JSON format.
        
    Returns:
        boolean
"""


def validate_model(model: Base, row: dict) -> bool:
    result = True

    # Short circuit if there are no keys to be processed.
    if not row.keys():
        return False

    # Validate the impending row to be added is a subset of the model.
    if not row.keys() <= model.__dict__.keys():
        result = False

    return result
