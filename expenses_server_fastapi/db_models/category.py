from sqlalchemy import Column, Integer, String
from expenses_server_fastapi.db import Base
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"
    id = Column(Integer, primary_key=True)
    name = Column(String, unique=True)
    expenses = relationship("Expenses", back_populates="category")
