from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import date
from sqlalchemy import func

from app.core.database import get_db

from app.models.auditeur import Auditeur
from app.models.prestataire import Prestataire
from app.models.plan import Plan
from app.models.affect import Affect
from app.models.audit import Audit

router = APIRouter()

@router.get("/kpis")
def get_dashboard_kpis(db: Session = Depends(get_db)):
    today = date.today()

    total_auditeurs = db.query(Auditeur).count()
    total_prestataires = db.query(Prestataire).count()

    auditeurs_occupees = (
        db.query(Auditeur)
        .join(Auditeur.affects)
        .distinct()
        .count()
    )

    taux_occupation = (auditeurs_occupees / total_auditeurs) * 100 if total_auditeurs > 0 else 0

    total_plans = db.query(Plan).count()
    audits_en_cours = db.query(Plan).filter(Plan.status == "EN COURS").count()
    audits_suspendu = db.query(Plan).filter(Plan.status == "SUSPENDU").count()
    audits_termines = db.query(Plan).filter(Plan.status == "TERMINE").count()

    total_affectations = db.query(Affect).count()

    affectations_actives = (
        db.query(Affect)
        .join(Affect.audit)
        .join(Audit.plans)
        .filter(Plan.date_debut <= today, Plan.date_fin >= today)
        .distinct()
        .count()
    )

    top_prestataires = (
        db.query(
            Prestataire.nom,
            func.count(Affect.id).label("nb_affects")
        )
        .join(Affect)
        .group_by(Prestataire.id)
        .order_by(func.count(Affect.id).desc())
        .limit(5)
        .all()
    )

    return {
        "auditeurs_total": total_auditeurs,
        "prestataires_total": total_prestataires,
        "taux_occupation_auditeurs": round(taux_occupation, 2),
        "plans_total": total_plans,
        "audits_en_cours": audits_en_cours,
        "audits_suspendu": audits_suspendu,
        "audits_termines": audits_termines,
        "affectations_total": total_affectations,
        "affectations_actives": affectations_actives,
        "top_prestataires": [
            {"nom": nom, "nb_affects": nb_affects}
            for nom, nb_affects in top_prestataires
        ]
    }

@router.get("/audits-par-mois")
def get_plans_by_month(db: Session = Depends(get_db)):
    results = (
        db.query(
            func.month(Plan.date_debut).label("mois"),
            func.count(Plan.id).label("nombre")
        )
        .group_by(func.month(Plan.date_debut))
        .order_by(func.month(Plan.date_debut))
        .all()
    )
    return [{"mois": mois, "nombre": nombre} for mois, nombre in results]

@router.get("/affect-prestataires")
def get_affect_prestataires(db: Session = Depends(get_db)):
    results = (
        db.query(Prestataire.nom, func.count(Affect.id).label("nb_affectations"))
        .join(Affect, Prestataire.id == Affect.prestataire_id)
        .group_by(Prestataire.nom)
        .order_by(func.count(Affect.id).desc())
        .limit(5)
        .all()
    )
    return [{"nom": nom, "affectations": nb} for nom, nb in results]

