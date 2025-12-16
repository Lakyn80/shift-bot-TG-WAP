from sqlalchemy import ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column

from app.db.base import Base


class ShiftAssignment(Base):
    __tablename__ = "shift_assignments"
    __table_args__ = (
        UniqueConstraint("shift_id", "user_id", name="uq_shift_user"),
    )

    id: Mapped[int] = mapped_column(primary_key=True)

    shift_id: Mapped[int] = mapped_column(ForeignKey("shifts.id"))
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
