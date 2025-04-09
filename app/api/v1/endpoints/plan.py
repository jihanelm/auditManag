import os
from io import BytesIO
from typing import Optional, List

import pandas as pd
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Query
from sqlalchemy import extract
from sqlalchemy.orm import Session
from starlette.responses import FileResponse

from app.core.database import get_db
from app.models.audit import Audit
from app.models.plan import Plan
from app.schemas.plan import PlanResponse
from app.services.plan import export_plans_to_excel, get_filtered_plans

from log_config import setup_logger

logger = setup_logger()

router = APIRouter()

@router.post("/upload")
async def upload_plan(file: UploadFile = File(...), db: Session = Depends(get_db)):
    if not file.filename.endswith((".xls", ".xlsx")):
        raise HTTPException(status_code=400, detail="Format de fichier non supporté. Veuillez uploader un fichier Excel.")

    try:
        contents = await file.read()
        df = pd.read_excel(BytesIO(contents))

        #columns_fixes = {"ref", "type_audit", "date_debut", "duree", "date_fin", "status", "remarques",
                         #"date_realisation"}
        #colonnes_dynamiques = set(df.columns) - columns_fixes

        required_columns = {"ref", "type_audit", "date_debut", "duree", "date_fin", "status", "remarques", "date_realisation"}
        if not required_columns.issubset(df.columns):
            raise HTTPException(status_code=400, detail=f"Colonnes manquantes: {required_columns - set(df.columns)}")

        # Supprimer les anciens plans si besoin :
        # db.query(Plan).delete()
        # db.commit()

        plans_to_insert = []
        for _, row in df.iterrows():
            plan = Plan(
                ref=row["ref"],
                type_audit=row["type_audit"],
                date_debut=row["date_debut"],
                date_realisation=row.get("date_realisation"),
                duree=row["duree"],
                date_fin=row["date_fin"],
                status=row["status"],
                remarques=row.get("remarques"),
            )
            """
            plan = Plan(
                ref=row["ref"],
                type_audit=row["type_audit"],
                date_debut=row["date_debut"],
                date_realisation=row.get("date_realisation"),
                duree=row["duree"],
                date_fin=row["date_fin"],
                status=row["status"],
                remarques=row.get("remarques"),
                extra_data=extra_data
            )
            """
            plans_to_insert.append(plan)

        db.bulk_save_objects(plans_to_insert)
        db.commit()

        return {"message": f"{len(plans_to_insert)} plans enregistrés avec succès !"}

    except Exception as e:
        print("Erreur lors de l'upload:", str(e))
        raise HTTPException(status_code=500, detail=f"Erreur de traitement du fichier: {str(e)}")


@router.put("/plans/{plan_id}/associate_audit/{audit_id}")
def associate_audit(plan_id: int, audit_id: int, db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    audit = db.query(Audit).filter(Audit.id == audit_id).first()

    if not plan:
        raise HTTPException(status_code=404, detail="Plan non trouvé")
    if not audit:
        raise HTTPException(status_code=404, detail="Audit non trouvé")

    plan.audit_id = audit.id
    db.commit()
    db.refresh(plan)

    return {"message": "Audit associé avec succès", "plan_id": plan.id, "audit_id": audit.id}

@router.get("/plans/download/")
def download_plans(
    db: Session = Depends(get_db),
    month: int = Query(None, ge=1, le=12),
    year: int = Query(None, ge=2000, le=2100),
):
    file_path = export_plans_to_excel(db, month, year)

    if not file_path or not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="Aucun plan trouvé pour cette période")

    return FileResponse(file_path, filename=os.path.basename(file_path), media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")


@router.get("/plans/", response_model=List[PlanResponse])
def get_plans(
        db: Session = Depends(get_db),
        month: Optional[int] = Query(None, ge=1, le=12),
        year: Optional[int] = Query(None, ge=2000, le=2100),
        status: Optional[str] = None,
        type_audit: Optional[str] = None,
        start_date: Optional[str] = None,
        end_date: Optional[str] = None
):
    plans = get_filtered_plans(
        db,
        month=month,
        year=year,
        status=status,
        type_audit=type_audit,
        start_date=start_date,
        end_date=end_date
    )

    return plans

"""@router.patch("/plans/{plan_id}/add_field")
def add_custom_field(plan_id: int, key: str, value: str, db: Session = Depends(get_db)):
    plan = db.query(Plan).filter(Plan.id == plan_id).first()
    if not plan:
        raise HTTPException(status_code=404, detail="Plan non trouvé")

    if not plan.extra_data:
        plan.extra_data = {}

    plan.extra_data[key] = value
    db.commit()
    db.refresh(plan)

    return {"message": "Champ personnalisé ajouté", "extra_data": plan.extra_data}"""



"""
@router.post("/plans/", response_model=PlanResponse)
def create_new_plan(plan_data: PlanBase, db: Session = Depends(get_db)):
    return create_plan(db, plan_data)

@router.get("/plans/{plan_id}", response_model=PlanResponse)
def read_plan(plan_id: int, db: Session = Depends(get_db)):
    plan = get_plan(db, plan_id)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return plan

@router.get("/plans/")
def get_plans_by_date(month: int, year: int, db: Session = Depends(get_db)):
    plans = get_plans_by_month(db, month, year)
    return plans

@router.put("/plans/{plan_id}/status")
def change_plan_status(plan_id: int, status: str, db: Session = Depends(get_db)):
    plan = update_plan_status(db, plan_id, status)
    if plan is None:
        raise HTTPException(status_code=404, detail="Plan not found")
    return {"message": "Plan status updated successfully"}
"""