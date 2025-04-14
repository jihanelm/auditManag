from typing import Optional

from pydantic import BaseModel
from datetime import date

class PlanBase(BaseModel):
    ref: str
    type_audit: str
    date_debut: date
    date_realisation: Optional[date] = None
    duree: int
    date_fin: date
    status: str
    remarques: Optional[str] = None

class PlanCreate(PlanBase):
    ref: str
    type_audit: str
    date_debut: date
    date_realisation: Optional[date]
    duree: int
    date_fin: date
    status: str
    remarques: Optional[str]
    audit_id: Optional[int] = None

class PlanResponse(PlanBase):
    id: int
    ref: str
    type_audit: str
    date_debut: date
    date_realisation: Optional[date]
    duree: int
    date_fin: date
    status: str
    remarques: Optional[str]
    audit_id: Optional[int]

    class Config:
        from_attributes = True

