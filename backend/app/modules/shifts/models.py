from sqlalchemy import Column, Integer, Date, Time, String
from sqlalchemy.orm import relationship

from app.db.base import Base


class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)

    name = Column(String, nullable=False)

    date = Column(Date, nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)

    location = Column(String, nullable=True)
    max_workers = Column(Integer, nullable=False, default=1)

    assignments = relationship("ShiftAssignment", back_populates="shift")
