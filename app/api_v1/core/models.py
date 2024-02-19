from typing import Annotated
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, ForeignKey, String, UniqueConstraint


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    subscription: Mapped[bool] = mapped_column(default=False)
    cost: Mapped[Numeric] = mapped_column(
        Numeric(precision=10, scale=2),
        default=0,
    )
    balance: Mapped[Numeric] = mapped_column(
        Numeric(precision=10, scale=2),
        default=0,
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


class Referral(Base):
    __tablename__ = "referrals"
    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(unique=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    # Добавляем отношение многие к одному с моделью User
    user: Mapped["User"] = relationship(back_populates="referrals")

    def __str__(self):
        return f"User(id={self.id!r})"

    def __repr__(self) -> str:
        return str(self)


class Key(Base):
    __tablename__ = "keys"
    id: Mapped[intpk]
    api_id: Mapped[int] = mapped_column(unique=True)
    name: Mapped[str] = mapped_column(String(25), unique=True, default=None)
    value: Mapped[str] = mapped_column(unique=True, default=None)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    user: Mapped["User"] = relationship(back_populates="key")

    __table_args__ = (UniqueConstraint("user_id"),)

    def __str__(self):
        return f"User(id={self.id!r})"

    def __repr__(self) -> str:
        return str(self)
