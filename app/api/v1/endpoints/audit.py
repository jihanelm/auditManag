from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.audit import AuditResponse
from app.models.audit import Audit
from app.services.audit import create_audit, get_all_audits, get_audit_by_id, save_uploaded_file

from log_config import setup_logger

logger = setup_logger()

router = APIRouter()

@router.post("/request", response_model=AuditResponse)
def create_audit_request(
    #user_id: int = Form(...),
    type_audit: str = Form(...),
    demandeur_nom: str = Form(...),
    demandeur_prenom: str = Form(...),
    demandeur_email: str = Form(...),
    demandeur_phone: str = Form(...),
    demandeur_departement: str = Form(...),
    description: str = Form(...),
    objectif: str = Form(...),
    urgence: str = Form(...),
    domain_name: str = Form(...),
    fichier_attache: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    logger.info("Réception de la requête de création d'audit par %s %s (%s)", demandeur_prenom, demandeur_nom,
                demandeur_email)

    audit = create_audit(
        type_audit, demandeur_nom, demandeur_prenom, demandeur_email,
        demandeur_phone, demandeur_departement, description, objectif, urgence, domain_name,
        fichier_attache, db
    )

    logger.info("Audit créé avec succès. ID: %s | Type: %s | État initial: %s", audit.id, audit.type_audit, audit.etat)

    return audit

@router.get("/", response_model=List[AuditResponse])
def get_audits(db: Session = Depends(get_db)):
    logger.info("Récupération de la liste des audits")
    audits = get_all_audits(db)
    logger.info("Nombre d'audits récupérés: %d", len(audits))
    return audits


@router.get("/{audit_id}", response_model=AuditResponse)
def get_audit(audit_id: int, db: Session = Depends(get_db)):
    logger.info("Recherche de l'audit avec l'ID: %d", audit_id)
    audit = get_audit_by_id(audit_id, db)
    if not audit:
        logger.warning("Audit non trouvé pour l'ID: %d", audit_id)
        raise HTTPException(status_code=404, detail="Audit not found")
    logger.info("Audit trouvé: ID %d | Type: %s | État: %s", audit.id, audit.type_audit, audit.etat)
    return audit

@router.patch("/{audit_id}/update-etat")
def update_audit_etat(audit_id: int, etat: str, db: Session = Depends(get_db)):
    logger.info("Mise à jour de l'état de l'audit ID %d vers: %s", audit_id, etat)
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if not audit:
        logger.error("Impossible de mettre à jour : audit ID %d non trouvé", audit_id)
        raise HTTPException(status_code=404, detail="Audit not found")

    audit.etat = etat
    db.commit()
    db.refresh(audit)
    logger.info("État mis à jour avec succès pour l'audit ID %d | Nouvel état: %s", audit.id, audit.etat)
    return audit
