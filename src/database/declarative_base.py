from decouple import config

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_user = config('DB_USER')
db_pass = config('DB_PASS')
db_host = config('DB_HOST')
db_database = config('DATABASE')

engine = create_engine('postgresql://'+db_user+':'+db_pass+'@'+db_host+'/'+db_database)
Session = sessionmaker(bind=engine)

Base = declarative_base()
Session = Session()
