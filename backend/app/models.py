from sqlalchemy import Column, Integer, String
from .database import Base

class nuke(Base):
    __tablename__ = 'nuke'
    id = Column(Integer,primary_key=True,nullable=False)
    xtra = Column(String,nullable=False)