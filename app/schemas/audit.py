from pydantic import BaseModel, EmailStr
from datetime import date
from typing import Optional

class AuditBase(BaseModel):
    type_audit: str
    demandeur_nom: str
    demandeur_prenom: str
    demandeur_email: EmailStr
    demandeur_phone: str
    demandeur_departement: str
    description: str
    objectif: str
    urgence: str
    fichier_attache: Optional[str] = None

"""
class AuditCreate(AuditBase):
    user_id: int
"""

class AuditResponse(AuditBase):
    id: int
    date_creation: date
    etat: str

    class Config:
        from_attributes = True
