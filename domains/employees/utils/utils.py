import string
import re

from sqlalchemy import exc


def get_or_create(session_fact, model, **kwargs):
    with session_fact() as session:
        with session.begin():
            try:
                result = session.query(model).filter_by(**kwargs).one()
                return result
            except exc.NoResultFound as E:
                result = model(**kwargs)
                session.add(result)
                session.commit()
                return result



