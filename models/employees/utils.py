from sqlalchemy import exc

# Gets or creates the specified row in the table. The
# session arg represents the session factory object.
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
