from typing import Annotated, TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import (
    ForeignKey,
    String,
    UniqueConstraint,
    BigInteger,
)


intpk = Annotated[int, mapped_column(primary_key=True)]

if TYPE_CHECKING:
    from .user import User


class Key(Base):
    __tablename__ = "keys"
    id: Mapped[intpk]

    api_id: Mapped[int] = mapped_column(
        BigInteger(),
        unique=True,
    )
    name: Mapped[str] = mapped_column(
        String(25),
        unique=True,
        default=None,
    )
    value: Mapped[str] = mapped_column(
        unique=True,
        default=None,
    )
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    user: Mapped["User"] = relationship(
        back_populates="key",
    )

    __table_args__ = (UniqueConstraint("user_id"),)

    def __str__(self):
        return f"User(id={self.id!r})"

    def __repr__(self) -> str:
        return str(self)
