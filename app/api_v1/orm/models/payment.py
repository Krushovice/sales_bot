from typing import Annotated, TYPE_CHECKING
from .base import Base
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import ForeignKey


intpk = Annotated[int, mapped_column(primary_key=True)]

if TYPE_CHECKING:
    from .user import User


class Payment(Base):
    __tablename__ = "payments"

    id: Mapped[intpk]

    payment_id: Mapped[int]

    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id", ondelete="CASCADE"),
    )
    # Добавляем отношение многие к одному с моделью User
    user: Mapped["User"] = relationship(
        back_populates="payments",
        lazy="selectin",
    )

    def __str__(self):
        return f"Payment(id={self.id!r}, payment_id={self.payment_id!r})"

    def __repr__(self) -> str:
        return str(self)
