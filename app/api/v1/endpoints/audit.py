from fastapi import APIRouter, Depends, HTTPException, File, UploadFile
from sqlalchemy.orm import Session
from app.schemas.audit import AuditCreate, AuditResponse
from app.core.database import get_db
from app.services.audit import create_audit_request

router = APIRouter()

@router.post("/audits/request", response_model=AuditResponse)
async def request_audit(
    audit_data: AuditCreate = Depends(),
    file: UploadFile = File(None),
    db: Session = Depends(get_db),
):
    """Endpoint pour créer une demande d'audit avec ou sans fichier attaché."""
    return create_audit_request(db, audit_data, file)
