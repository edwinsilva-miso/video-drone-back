from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship

from src.database.declarative_base import Base
from src.models import Role, Video


class User(Base):
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True)
    fullname = Column(String)
    username = Column(String)
    password = Column("pass", String)
    role_id = Column(ForeignKey("roles.id"))
    email = Column(String)

    role = relationship('Role', back_populates="users")

    videos = relationship('Video', back_populates='user', cascade='all, delete, delete-orphan')
