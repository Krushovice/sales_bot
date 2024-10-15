from typing import Annotated, TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey, BigInteger


intpk = Annotated[int, mapped_column(primary_key=True)]

if TYPE_CHECKING:
    from .user import User


class Referral(Base):
    __tablename__ = "referrals"
    id: Mapped[intpk]
    tg_id: Mapped[int] = mapped_column(BigInteger(), unique=True)

    user_id: Mapped[int] = mapped_column(
        BigInteger(),
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    # Добавляем отношение многие к одному с моделью User
    user: Mapped["User"] = relationship(
        back_populates="referrals",
        lazy="selectin",
    )

    def __str__(self):
        return f"User(tg_id={self.tg_id!r})"

    def __repr__(self) -> str:
        return str(self)
