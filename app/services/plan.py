from typing import Optional

import pandas as pd
from sqlalchemy import extract
from sqlalchemy.orm import Session
from app.models.audit import Audit
from app.models.plan import Plan
from app.schemas.audit import AuditBase, AuditResponse
from app.schemas.plan import PlanBase, PlanResponse

from log_config import setup_logger

logger = setup_logger()

def export_plans_to_excel(db: Session, month: int = None, year: int = None):
    query = db.query(Plan)

    if year:
        query = query.filter(extract('year', Plan.date_debut) == year)
    if month:
        query = query.filter(extract('month', Plan.date_debut) == month)

    plans = query.all()

    if not plans:
        return None

    data = [
        {
            "ID": plan.id,
            "Référence": plan.ref,
            "Type Audit": plan.type_audit,
            "Date Début": plan.date_debut,
            "Date Réalisation": plan.date_realisation,
            "Durée (jours)": plan.duree,
            "Date Fin": plan.date_fin,
            "Statut": plan.status,
            "Remarques": plan.remarques,
            "Audit ID": plan.audit_id,
        }
        for plan in plans
    ]

    df = pd.DataFrame(data)
    file_path = f"plans_{year}_{month}.xlsx" if month else f"plans_{year}.xlsx"
    df.to_excel(file_path, index=False)

    return file_path

def get_filtered_plans(
    db: Session,
    month: Optional[int] = None,
    year: Optional[int] = None,
    status: Optional[str] = None,
    type_audit: Optional[str] = None,
    start_date: Optional[str] = None,
    end_date: Optional[str] = None
):
    query = db.query(Plan)

    if year:
        query = query.filter(extract('year', Plan.date_debut) == year)
    if month:
        query = query.filter(extract('month', Plan.date_debut) == month)
    if status:
        query = query.filter(Plan.status == status)
    if type_audit:
        query = query.filter(Plan.type_audit == type_audit)
    if start_date:
        query = query.filter(Plan.date_debut >= start_date)
    if end_date:
        query = query.filter(Plan.date_debut <= end_date)

    return query.all()









"""def create_plan(db: Session, plan_data: PlanBase) -> PlanResponse:
    new_plan = Plan(**plan_data.dict())
    db.add(new_plan)
    db.commit()
    db.refresh(new_plan)
    return new_plan

def get_plan(db: Session, plan_id: int) -> PlanResponse:
    return db.query(Plan).filter(Plan.id == plan_id).first()

def get_plans_by_month(db: Session, month: int, year: int):
    return db.query(Plan).filter(Plan.date_realisation.year == year, Plan.date_realisation.month == month).all()

def update_plan_status(db: Session, plan_id: int, status: str):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if plan:
        plan.status = status
        db.commit()
        db.refresh(plan)
    return plan
"""