from typing import Annotated, TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, String, BigInteger


intpk = Annotated[int, mapped_column(primary_key=True)]
if TYPE_CHECKING:
    from .referral import Referral
    from .key import Key


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True)
    username: Mapped[str] = mapped_column(
        String(30),
        unique=True,
        nullable=True,
    )
    subscription: Mapped[bool] = mapped_column(default=False)
    cost: Mapped[Numeric] = mapped_column(
        Numeric(precision=10, scale=2),
        default=0,
    )
    balance: Mapped[Numeric] = mapped_column(
        Numeric(precision=10, scale=2),
        default=0,
    )
    discount: Mapped[int] = mapped_column(
        default=0,
        nullable=True,
    )
    subscribe_date: Mapped[str] = mapped_column(
        nullable=True,
    )
    expiration_date: Mapped[str] = mapped_column(
        nullable=True,
    )
    referrals: Mapped[list["Referral"]] = relationship(
        back_populates="user",
        lazy="selectin",
        cascade="all, delete-orphan",
    )
    key: Mapped["Key"] = relationship(
        back_populates="user",
        lazy="selectin",
    )

    def __str__(self):
        return f"User(id={self.id!r}, username={self.username!r})"

    def __repr__(self) -> str:
        return str(self)
