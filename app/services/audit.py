import os
import shutil

from fastapi import UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
from app.models.audit import Audit
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from log_config import setup_logger

logger = setup_logger()

UPLOAD_DIR = "uploads"
PDF_DIR = "pdf_reports"
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(PDF_DIR, exist_ok=True)

def save_uploaded_file(uploaded_file: UploadFile) -> str:
    """Saves an uploaded file and returns its normalized path."""

    # S'assurer que le dossier de destination existe
    os.makedirs(UPLOAD_DIR, exist_ok=True)

    # Construire le chemin avec os.path.join (Windows mettra \ par défaut)
    file_path = os.path.join(UPLOAD_DIR, uploaded_file.filename)

    try:
        with open(file_path, "wb") as buffer:
            shutil.copyfileobj(uploaded_file.file, buffer)

        # Normaliser le chemin pour éviter les problèmes avec les URLs
        normalized_path = file_path.replace("\\", "/")  # Convertir \ en /
        logger.info("Fichier '%s' enregistré avec succès à l'emplacement : %s", uploaded_file.filename, normalized_path)
        return normalized_path

    except Exception as e:
        logger.error("Erreur lors de l'enregistrement du fichier '%s' : %s", uploaded_file.filename, str(e))
        return None

def generate_audit_pdf(audit: Audit) -> str:
    """Generates a PDF report for the given audit."""
    pdf_path = os.path.join(PDF_DIR, f"audit_{audit.id}.pdf")
    try:
        c = canvas.Canvas(pdf_path, pagesize=A4)
        c.setFont("Helvetica", 12)

        y_position = 800
        c.drawString(100, y_position, "Audit Request Summary")
        c.line(100, y_position - 5, 400, y_position - 5)
        y_position -= 30

        details = [
            ("Audit ID", audit.id),
            #("User ID", audit.user_id),
            ("Type", audit.type_audit),
            ("Requester Name", f"{audit.demandeur_nom} {audit.demandeur_prenom}"),
            ("Email", audit.demandeur_email),
            ("Phone", audit.demandeur_phone),
            ("Department", audit.demandeur_departement),
            ("Description", audit.description),
            ("Objective", audit.objectif),
            ("Urgency", audit.urgence),
            ("Domain Name", audit.domain_name),
            ("Attached File", audit.fichier_attache if audit.fichier_attache else "None"),
        ]

        for label, value in details:
            c.drawString(100, y_position, f"{label}: {value}")
            y_position -= 20

        c.save()
        logger.info("La fiche de la demande est généré avec succès pour l'audit ID %d à l'emplacement : %s", audit.id, pdf_path)
        return pdf_path
    except Exception as e:
        logger.error("Erreur lors de la generation de la fiche de la demande pour l'audit ID %d : %s", (audit.id, str(e)))


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
        domain_name: str,
        fichier_attache: Optional[UploadFile],
        db: Session
) -> Audit:
    logger.info("Début de la création d'un audit par %s %s (%s)", demandeur_prenom, demandeur_nom, demandeur_email)

    file_path = None
    if fichier_attache:
        logger.info("Un fichier attaché a été fourni : %s", fichier_attache.filename)
        file_path = save_uploaded_file(fichier_attache)

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
        domain_name=domain_name,
        fichier_attache=file_path
    )
    db.add(audit)
    db.commit()
    db.refresh(audit)

    logger.info("Audit inséré en base avec l'ID : %d", audit.id)

    # Generate PDF report
    pdf_path = generate_audit_pdf(audit)
    audit.pdf_report_path = pdf_path
    db.commit()

    logger.info("Création de l'audit terminée avec succès. PDF associé : %s", pdf_path)
    return audit


def get_all_audits(db: Session) -> List[Audit]:
    audits = db.query(Audit).all()
    logger.info("Récupération de tous les audits. Total : %d", len(audits))
    return audits


def get_audit_by_id(audit_id: int, db: Session) -> Optional[Audit]:
    audit = db.query(Audit).filter(Audit.id == audit_id).first()
    if audit:
        logger.info("Audit trouvé pour l'ID %d", audit_id)
    else:
        logger.warning("Aucun audit trouvé pour l'ID %d", audit_id)
    return audit