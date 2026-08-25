from uuid import UUID, uuid4
from sqlalchemy import String, types
from sqlalchemy.orm import MappedColumn as Mapped, mapped_column
from .core import Base


class User(Base):
    __tablename__ = "users"

    username: Mapped[str] = mapped_column(String, nullable=False, unique=True)
    password_hash: Mapped[str] = mapped_column(String, nullable=False)
    id: Mapped[UUID] = mapped_column(
        types.UUID,
        default_factory=uuid4,
        primary_key=True,
    )
