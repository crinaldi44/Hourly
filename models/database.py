from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from flask import current_app

# Create a new SQLAlchemy engine with URI for MySQL database.
# The pattern to initiate connectivity is: create a session at
# the start of a web request, call Session.commit(), and then
# close the session at the end of the request. The general
# preferred practice is to use the 'with' keyword.
engine = create_engine('mysql+pymysql://crinaldi:7539mmr@localhost:3306/hourly', echo=True)
Session = sessionmaker(bind=engine)
Base = declarative_base()