from pydantic import BaseModel
from datetime import date

class PlanBase(BaseModel):
    ref: str
    type_audit: str
    date_debut: date
    date_realisation: date
    duree: int
    date_fin: date
    status: str
    remarques: str

class PlanCreate(PlanBase):
    audit_id: int

class PlanResponse(PlanBase):
    id: int

    class Config:
        orm_mode = True
