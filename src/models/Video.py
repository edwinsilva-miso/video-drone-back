from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database.declarative_base import Base


class Video(Base):
    __tablename__ = 'videos'

    id = Column(Integer, primary_key=True)
    description = Column(String)
    path = Column(String)
    user_id = Column(ForeignKey("users.id"))

    user = relationship('User', back_populates='videos')
