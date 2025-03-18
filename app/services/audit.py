from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import UploadFile
import shutil
import os
from app.models.audit import Audit
from app.schemas.audit import AuditCreate
from datetime import date

UPLOAD_DIR = "uploads"

def create_audit_request(db: Session, audit_data: AuditCreate, file: UploadFile = None):
    """Service permettant de créer une demande d'audit."""

    # Gérer l'upload du fichier
    file_path = None
    if file:
        if not os.path.exists(UPLOAD_DIR):
            os.makedirs(UPLOAD_DIR)
        file_path = os.path.join(UPLOAD_DIR, file.filename)
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(file.file, buffer)

    new_audit = Audit(
        date_creation=date.today(),
        type_audit=audit_data.type_audit,
        demandeur_nom=audit_data.demandeur_nom,
        demandeur_prenom=audit_data.demandeur_prenom,
        demandeur_email=audit_data.demandeur_email,
        demandeur_phone=audit_data.demandeur_phone,
        demandeur_departement=audit_data.demandeur_departement,
        description=audit_data.description,
        objectif=audit_data.objectif,
        urgence=audit_data.urgence,
        fichier_attache=file_path,
        user_id=audit_data.user_id,
        etat="En attente"
    )

    try:
        db.add(new_audit)
        db.commit()
        db.refresh(new_audit)
        return new_audit
    except IntegrityError:
        db.rollback()
        raise ValueError("Erreur lors de la création de la demande d'audit.")
