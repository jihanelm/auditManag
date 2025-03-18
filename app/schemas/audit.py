from pydantic import BaseModel
from datetime import date


class AuditBase(BaseModel):
    date_creation: date
    type_audit: str


class AuditCreate(AuditBase):
    user_id: int



class AuditResponse(AuditBase):
    id: int
    etat: str

    class Config:
        from_attributes = True

