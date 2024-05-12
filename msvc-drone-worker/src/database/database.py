import datetime
import os

from sqlalchemy import create_engine, Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

db_path = os.environ.get('DATABASE_URL')

engine = create_engine(db_path)
Session = sessionmaker(bind=engine)

Base = declarative_base()


def open_session():
    return Session()


class ProcessingTask(Base):
    __tablename__ = 'processing_task'

    video_id = Column(String, primary_key=True)
    create_time = Column(DateTime, default=datetime.datetime.now)
