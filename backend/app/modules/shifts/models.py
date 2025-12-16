from sqlalchemy import Date, Time, String, Enum, Integer
from sqlalchemy.orm import Mapped, mapped_column
import enum

from app.db.base import Base


class ShiftStatus(enum.Enum):
    open = "open"
    full = "full"
    cancelled = "cancelled"
    closed = "closed"


class Shift(Base):
    __tablename__ = "shifts"

    id: Mapped[int] = mapped_column(primary_key=True)

    date: Mapped[str] = mapped_column(Date)
    start_time: Mapped[str] = mapped_column(Time)
    end_time: Mapped[str] = mapped_column(Time)

    location: Mapped[str] = mapped_column(String(100))
    max_workers: Mapped[int] = mapped_column(Integer)

    status: Mapped[ShiftStatus] = mapped_column(
        Enum(ShiftStatus), default=ShiftStatus.open
    )
