import os

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
    domain_name: str
    fichier_attache: Optional[str] = None

"""
class AuditCreate(AuditBase):
    user_id: int
"""

class AuditResponse(AuditBase):
    id: int
    date_creation: date
    etat: str
    pdf_report_path: Optional[str] = None

    @property
    def fichier_url(self):
        if self.fichier_attache:
            # Remplace les backslashes par des slashes pour une URL correcte
            return f"http://localhost:8000/{self.fichier_attache.replace(os.sep, '/')}"
        return None

    class Config:
        from_attributes = True
