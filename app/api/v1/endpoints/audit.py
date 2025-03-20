from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from sqlalchemy.orm import Session
from typing import List, Optional
from app.core.database import get_db
from app.schemas.audit import AuditResponse
from app.services.audit import create_audit, get_all_audits, get_audit_by_id

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
    fichier_attache: Optional[UploadFile] = File(None),
    db: Session = Depends(get_db),
):
    file_bytes = fichier_attache.file.read() if fichier_attache else None
    fichier_name = fichier_attache.filename if fichier_attache else None

    audit = create_audit(
        type_audit, demandeur_nom, demandeur_prenom, demandeur_email,
        demandeur_phone, demandeur_departement, description, objectif, urgence,
        file_bytes, fichier_name, db
    )

    """
    audit = create_audit(
        user_id, type_audit, demandeur_nom, demandeur_prenom, demandeur_email,
        demandeur_phone, demandeur_departement, description, objectif, urgence,
        file_bytes, fichier_name, db
    )
    """

    return audit


@router.get("/", response_model=List[AuditResponse])
def get_audits(db: Session = Depends(get_db)):
    return get_all_audits(db)


@router.get("/{audit_id}", response_model=AuditResponse)
def get_audit(audit_id: int, db: Session = Depends(get_db)):
    audit = get_audit_by_id(audit_id, db)
    if not audit:
        raise HTTPException(status_code=404, detail="Audit not found")
    return audit
