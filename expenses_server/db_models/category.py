from sqlalchemy.orm import mapped_column, Mapped
from .core import Base
from sqlalchemy.orm import relationship


class Category(Base):
    __tablename__ = "categories"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(unique=True)
    expenses = relationship("Expense", back_populates="category")
