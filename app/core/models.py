from typing import Annotated
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import BigInteger, Numeric, ForeignKey


intpk = Annotated[int, mapped_column(primary_key=True)]
str_255 = Annotated[str, 255]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)
    subscription: Mapped[bool] = False
    cost: Mapped[Numeric] = mapped_column(Numeric(precision=10, scale=2))
    balance: Mapped[Numeric] = mapped_column(Numeric(precision=10, scale=2))
    referals: Mapped[list["Referral"]] = relationship(
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __str__(self):
        return f"User(id={self.id!r}, name={self.name!r}, username={self.username!r})"

    def __repr__(self) -> str:
        return str(self)


class Referral(Base):
    __tablename__ = 'referrals'
    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(unique=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    # Добавляем отношение многие к одному с моделью User
    user: Mapped['User'] = relationship(
        back_populates="referrals"
        )

    def __str__(self):
        return f"User(id={self.id!r}, name={self.name!r}, username={self.username!r})"

    def __repr__(self) -> str:
        return str(self)
