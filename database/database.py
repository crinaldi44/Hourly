from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import current_app as app

# Create a new SQLAlchemy engine with URI for PostgreSQL database.
# The pattern to initiate connectivity is: create a session at
# the start of a web request, call Session.commit(), and then
# close the session at the end of the request. The general
# preferred practice is to use the 'with' keyword.
engine = create_engine(
    "postgresql://chris:D41QYbmhlrjIXuQfJiQ4@hourly-postgres-prod.cicovww9r07h.us-east-1.rds.amazonaws.com:5432/employees", echo=False)
Session = sessionmaker(bind=engine)
Base = declarative_base()
