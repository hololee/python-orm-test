from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column


class Base(DeclarativeBase):
    pass


class Users(Base):
    __tablename__ = "users"
    id: Mapped[int] = mapped_column(primary_key=True)
    name: Mapped[str] = mapped_column(String)
    age: Mapped[int] = mapped_column(Integer)
    sex: Mapped[int] = mapped_column(Integer)
    region: Mapped[str] = mapped_column(String)

    def __repr__(self) -> str:
        return f"Users(id={self.id}, name={self.name}, age={self.age}, sex={self.sex}, region = {self.region})"
