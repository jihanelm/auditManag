from sqlalchemy.orm import Session
from app.models.audit import Audit
from app.schemas.audit import AuditCreate
from datetime import date


def create_audit_request(db: Session, audit_data: AuditCreate):
    """Service permettant de créer une demande d'audit."""
    new_audit = Audit(
        date_creation=date.today(),
        type_audit=audit_data.type_audit,
        user_id=audit_data.user_id,
        etat="En attente"
    )

    db.add(new_audit)
    db.commit()
    db.refresh(new_audit)
    return new_audit

