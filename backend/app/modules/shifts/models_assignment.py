from sqlalchemy import Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from app.db.base import Base


class ShiftAssignment(Base):
    __tablename__ = "shift_assignments"

    id = Column(Integer, primary_key=True, index=True)

    shift_id = Column(Integer, ForeignKey("shifts.id"), nullable=False)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)

    shift = relationship("Shift", back_populates="assignments")
