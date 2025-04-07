import os

from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.models.affect import Affect
from app.models.auditeur import Auditeur
from app.models.ip import IP
from app.models.prestataire import Prestataire
from app.schemas.affect import AffectSchema
from app.schemas.auditeur import AuditeurSchema
from app.schemas.prestataire import PrestataireSchema


def generate_affect_pdf(affect):
    pdf_dir = "affectations_pdfs"
    os.makedirs(pdf_dir, exist_ok=True)

    # Nom du fichier PDF
    pdf_filename = f"affect_{affect.id}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_filename)

    # Création du PDF
    c = canvas.Canvas(pdf_path, pagesize=A4)
    width, height = A4

    # Titre
    c.setFont("Helvetica-Bold", 16)
    c.drawString(200, height - 50, "Fiche d'Affectation d'Audit")

    # Informations générales
    c.setFont("Helvetica", 12)
    c.drawString(50, height - 100, f"ID Audit: {affect.audit_id}")
    c.drawString(50, height - 120, f"Prestataire: {affect.prestataire.nom}")
    c.drawString(50, height - 140, f"Date d'affectation: {affect.date_affectation.strftime('%d/%m/%Y')}")

    # Vérification que l'audit est bien attaché à l'affectation
    if hasattr(affect, 'audit') and affect.audit:
        # Informations sur le demandeur de l'audit
        y = height - 170
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Informations du Demandeur:")
        c.setFont("Helvetica", 11)
        y -= 20
        c.drawString(70, y, f"Nom: {affect.audit.demandeur_nom}")
        y -= 20
        c.drawString(70, y, f"Prénom: {affect.audit.demandeur_prenom}")
        y -= 20
        c.drawString(70, y, f"Email: {affect.audit.demandeur_email}")
        y -= 20
        c.drawString(70, y, f"Téléphone: {affect.audit.demandeur_phone}")

    # Liste des Auditeurs
    if hasattr(affect, 'auditeurs') and isinstance(affect.auditeurs, list):
        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "Liste des Auditeurs:")
        y -= 20
        for auditeur in affect.auditeurs:
            c.setFont("Helvetica-Bold", 12)
            c.drawString(70, y, f"Auditeur:")
            y -= 20
            c.setFont("Helvetica", 11)
            c.drawString(80, y, f"Nom: {auditeur.nom}")
            y -= 20
            c.drawString(80,y,f"Prenom: {auditeur.prenom}")
            y -= 20
            c.drawString(80,y,f"Email: {auditeur.email}")
            y -= 20
            c.drawString(80,y,f"Phone: {auditeur.phone}")
            y -= 20

    # Liste des IPs affectées
    if hasattr(affect, 'ips') and isinstance(affect.ips, list):
        y -= 30
        c.setFont("Helvetica-Bold", 12)
        c.drawString(50, y, "IPs affectées:")
        c.setFont("Helvetica", 11)
        y -= 20
        for ip in affect.ips:
            c.drawString(70, y, f"- {ip.adresse_ip}:{ip.port}")
            y -= 20

    # Sauvegarde du PDF
    c.save()

    return pdf_path.replace("\\", "/")

def create_affect(db: Session, affect_data: AffectSchema):
    affect = Affect(
        audit_id=affect_data.audit_id,
        prestataire_id=affect_data.prestataire_id
    )
    db.add(affect)
    db.commit()
    db.refresh(affect)

    for auditeur_data in affect_data.auditeurs:
        existing_auditeur = db.query(Auditeur).filter(
            Auditeur.email == auditeur_data.email
        ).first()

        if not existing_auditeur:
            auditeur = Auditeur(
                nom=auditeur_data.nom,
                prenom=auditeur_data.prenom,
                email=auditeur_data.email,
                phone=auditeur_data.phone,
                prestataire_id=auditeur_data.prestataire_id
            )
            db.add(auditeur)
            db.commit()
            db.refresh(auditeur)
            affect.auditeurs.append(auditeur)
        else:
            affect.auditeurs.append(existing_auditeur)

    for ip_data in affect_data.ips:
        existing_ip = db.query(IP).filter(
            IP.adresse_ip == ip_data.adresse_ip,
            IP.port == ip_data.port
        ).first()

        if not existing_ip:
            ip = IP(
                adresse_ip=ip_data.adresse_ip,
                port=int(ip_data.port),
                affect_id=affect.id,
                status="open"
            )
            db.add(ip)
            db.commit()
            db.refresh(ip)
            affect.ips.append(ip)
        else:
            affect.ips.append(existing_ip)

        affectationpath = generate_affect_pdf(affect)
        affect.affectationpath = affectationpath
        db.commit()

    return affect

def get_affect(db: Session, affect_id: int):
    return db.query(Affect).filter(Affect.id == affect_id).first()

def list_affects(db: Session):
    return db.query(Affect).all()

def create_auditeur(db: Session, auditeur_data: AuditeurSchema):
    auditeur = Auditeur(
        nom=auditeur_data.nom,
        prenom=auditeur_data.prenom,
        email=auditeur_data.email,
        phone=auditeur_data.phone,
        prestataire_id=auditeur_data.prestataire_id
    )
    db.add(auditeur)
    db.commit()
    db.refresh(auditeur)
    return auditeur

def create_prestataire(db: Session, prestataire_data: PrestataireSchema):
    prestataire = Prestataire(
        nom=prestataire_data.nom
    )
    db.add(prestataire)
    db.commit()
    db.refresh(prestataire)
    return prestataire

def list_auditeurs(db: Session):
    return db.query(Auditeur).all()

def list_ips(db: Session):
    return db.query(IP).all()

def delete_auditeur(db: Session, auditeur_id: int):
    auditeur = db.query(Auditeur).filter(Auditeur.id == auditeur_id).first()
    if not auditeur:
        return None

    for affect in auditeur.affects:
        affect.auditeurs.remove(auditeur)

    db.delete(auditeur)
    db.commit()
    return auditeur

def update_auditeur(db: Session, auditeur_id: int, auditeur_data: AuditeurSchema):
    auditeur = db.query(Auditeur).filter(Auditeur.id == auditeur_id).first()
    if not auditeur:
        return None

    auditeur.nom = auditeur_data.nom
    auditeur.prenom = auditeur_data.prenom
    auditeur.email = auditeur_data.email
    auditeur.phone = auditeur_data.phone
    auditeur.prestataire_id = auditeur_data.prestataire_id

    db.commit()
    db.refresh(auditeur)
    return auditeur
