import os
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.audit import Audit

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


def create_audit(
    #user_id: int,
    type_audit: str,
    demandeur_nom: str,
    demandeur_prenom: str,
    demandeur_email: str,
    demandeur_phone: str,
    demandeur_departement: str,
    description: str,
    objectif: str,
    urgence: str,
    fichier_attache: Optional[bytes],
    fichier_name: Optional[str],
    db: Session
) -> Audit:
    file_path = None
    if fichier_attache and fichier_name:
        file_path = os.path.join(UPLOAD_DIR, fichier_name)
        with open(file_path, "wb") as buffer:
            buffer.write(fichier_attache)

    audit = Audit(
        #user_id=user_id,
        type_audit=type_audit,
        demandeur_nom=demandeur_nom,
        demandeur_prenom=demandeur_prenom,
        demandeur_email=demandeur_email,
        demandeur_phone=demandeur_phone,
        demandeur_departement=demandeur_departement,
        description=description,
        objectif=objectif,
        urgence=urgence,
        fichier_attache=file_path
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)
    return audit


def get_all_audits(db: Session) -> List[Audit]:
    return db.query(Audit).all()


def get_audit_by_id(audit_id: int, db: Session) -> Optional[Audit]:
    return db.query(Audit).filter(Audit.id == audit_id).first()
