from shared.database import Base
from sqlalchemy import Column, Integer, String

class SimpleOBjectDB(Base):
    __tablename__ = "simple_object"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)