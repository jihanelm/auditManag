from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.audit import AuditCreate, AuditResponse
from app.core.database import get_db
from app.services.audit import create_audit_request

router = APIRouter()

@router.post("/request", response_model=AuditResponse)
def create_audit_request_endpoint(audit_data: AuditCreate, db: Session = Depends(get_db)):
    return create_audit_request(db, audit_data)
