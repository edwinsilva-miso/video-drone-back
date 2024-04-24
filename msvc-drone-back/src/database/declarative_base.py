import os

from decouple import config

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = config('DB_USER')
db_pass = config('DB_PASS')
db_host = config('DB_HOST')
db_database = config('DATABASE')
db_path = os.environ.get('DATABASE_URL')

engine = create_engine(db_path)
Session = sessionmaker(bind=engine)

Base = declarative_base()
Session = Session()
