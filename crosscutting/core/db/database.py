from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base

from crosscutting.core.config.config import config

engine = create_engine(
    config.POSTGRES_URI, echo=config.MODE == "dev")
Session = sessionmaker(bind=engine)
Base = declarative_base()
Base.metadata.create_all(engine)
