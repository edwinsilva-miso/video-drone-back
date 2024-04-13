import datetime
import sqlalchemy
from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from src.database.declarative_base import Base
import enum


class StatusVideo(enum.Enum):
    processed = "processed"
    uploaded = "uploaded"


class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    path = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))
    video_id = Column(String)
    status = Column(sqlalchemy.Enum(StatusVideo))
    timestamp = Column(DateTime, default=datetime.datetime.now())

    user = relationship('User', back_populates='videos')
