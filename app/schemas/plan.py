from typing import Optional, Dict, Any

from pydantic import BaseModel
from datetime import date

class PlanBase(BaseModel):
    #ref: str
    type_audit: str
    date_debut: date
    date_realisation: Optional[date] = None
    duree: int
    date_fin: date
    status: str
    remarques: Optional[str] = None

class PlanCreate(PlanBase):
    date_debut: date
    date_realisation: Optional[date]
    duree: int
    date_fin: date
    status: str
    audit_id: Optional[int] = None
    extra_data: Optional[Dict[str, Any]] = None

class PlanResponse(PlanBase):
    id: int
    ref: str
    audit_id: Optional[int]
    extra_data: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True

