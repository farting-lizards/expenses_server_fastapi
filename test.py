from sqlalchemy.orm import (
    Mapped,
    DeclarativeBase,
    MappedAsDataclass,
    relationship,
    mapped_column,
)


class Base(MappedAsDataclass, DeclarativeBase):
    pass


class Role(Base):
    __tablename__ = "roles"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, init=False)
    name: Mapped[str]
    role: Mapped[Role] = relationship("Role", back_populates="roles", init=False)


my_role = Role(name="somerole")
my_user = User(name="User1")
