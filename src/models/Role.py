from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from src.database.declarative_base import Base


class Role(Base):
    __tablename__ = 'roles'

    id = Column(Integer, primary_key=True)
    role_name = Column(String)
    description = Column(String)

    users = relationship('User', back_populates='role', cascade='all, delete, delete-orphan')
