from typing import Annotated
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import Numeric, ForeignKey, String


intpk = Annotated[int, mapped_column(primary_key=True)]


class User(Base):
    __tablename__ = "users"

    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)
    subscription: Mapped[bool] = False
<<<<<<< HEAD:app/api_v1/core/models.py
    cost: Mapped[Numeric] = mapped_column(Numeric(precision=10,
                                                  scale=2),
                                          nullable=True,
                                          )
    balance: Mapped[Numeric] = mapped_column(Numeric(precision=10,
                                                     scale=2),
                                             nullable=True)
    referrals: Mapped[list["Referral"]] = relationship(
=======
    cost: Mapped[Numeric] = mapped_column(Numeric(precision=10, scale=2))
    balance: Mapped[Numeric] = mapped_column(Numeric(precision=10, scale=2))
    referals: Mapped[list["Referral"]] = relationship(
>>>>>>> 198d5a0c5747c8ead75dd1248f5068b3a0233f2c:app/core/models.py
        back_populates="user",
        cascade="all, delete-orphan",
    )

    def __str__(self):
<<<<<<< HEAD:app/api_v1/core/models.py
        return f"User(id={self.id!r}, username={self.username!r})"
=======
        return f"User(id={self.id!r}, name={self.name!r}, username={self.username!r})"
>>>>>>> 198d5a0c5747c8ead75dd1248f5068b3a0233f2c:app/core/models.py

    def __repr__(self) -> str:
        return str(self)


class Referral(Base):
    __tablename__ = 'referrals'
    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(unique=True)
    username: Mapped[str] = mapped_column(String(30), unique=True)

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    # Добавляем отношение многие к одному с моделью User
    user: Mapped['User'] = relationship(
        back_populates="referrals"
        )

    def __str__(self):
<<<<<<< HEAD:app/api_v1/core/models.py
        return f"User(id={self.id!r}, username={self.username!r})"
=======
        return f"User(id={self.id!r}, name={self.name!r}, username={self.username!r})"
>>>>>>> 198d5a0c5747c8ead75dd1248f5068b3a0233f2c:app/core/models.py

    def __repr__(self) -> str:
        return str(self)
