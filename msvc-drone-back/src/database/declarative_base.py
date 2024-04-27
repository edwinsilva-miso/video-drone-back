import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_path = os.environ.get('DATABASE_URL')

engine = create_engine(db_path)
Session = sessionmaker(bind=engine)

Base = declarative_base()


def open_session():
    return Session()
