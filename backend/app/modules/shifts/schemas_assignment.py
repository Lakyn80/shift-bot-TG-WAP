from pydantic import BaseModel


class ShiftAssignmentCreate(BaseModel):
    shift_id: int
    user_id: int


class ShiftAssignmentRead(BaseModel):
    id: int
    shift_id: int
    user_id: int

    class Config:
        from_attributes = True
