from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

# Create a new SQLAlchemy engine with URI for PostgreSQL models.
# The pattern to initiate connectivity is: create a session at
# the start of a web request, call Session.commit(), and then
# close the session at the end of the request. The general
# preferred practice is to use the 'with' keyword.
engine = create_engine(
    "postgresql://crinaldi:test123@0.0.0.0:5432/employees", echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(engine)
