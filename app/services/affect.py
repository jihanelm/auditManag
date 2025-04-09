import os

from sqlalchemy.orm import Session
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas

from app.models.affect import Affect
from app.models.auditeur import Auditeur
from app.models.ip import IP
from app.models.ports import Port
from app.models.prestataire import Prestataire
from app.schemas.affect import AffectSchema
from app.schemas.auditeur import AuditeurSchema
from app.schemas.prestataire import PrestataireSchema

from log_config import setup_logger

logger = setup_logger()

def generate_affect_pdf(affect):
    logger.info(f"Génération du PDF pour l'affectation ID={affect.id}")
    pdf_dir = "affectations_pdfs"
    os.makedirs(pdf_dir, exist_ok=True)

    # Nom du fichier PDF
    pdf_filename = f"affect_{affect.id}.pdf"
    pdf_path = os.path.join(pdf_dir, pdf_filename)

    try:
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
            logger.debug("Ajout des infos du demandeur au PDF")
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
            logger.debug(f"{len(affect.auditeurs)} auditeurs ajoutés au PDF")
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
            logger.debug(f"{len(affect.ips)} IPs ajoutées au PDF")
            y -= 30
            c.setFont("Helvetica-Bold", 12)
            c.drawString(50, y, "IPs affectées:")
            c.setFont("Helvetica", 11)
            y -= 20
            for ip in affect.ips:
                for port in ip.ports:
                    c.drawString(70, y, f"- {ip.adresse_ip}:{port.numero} ({port.status})")
                    y -= 20

        # Sauvegarde du PDF
        c.save()
        logger.info(f"PDF généré avec succès : {pdf_path}")

        return pdf_path.replace("\\", "/")
    except Exception as e:
        logger.error(f"Erreur lors de la génération du PDF : {e}", exc_info=True)
        raise

def create_affect(db: Session, affect_data: AffectSchema):
    logger.info("Création d'une nouvelle affectation d'audit")
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
            logger.debug(f"Création du nouvel auditeur : {auditeur_data.email}")
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
            logger.debug(f"Auditeur déjà existant trouvé : {existing_auditeur.email}")
            affect.auditeurs.append(existing_auditeur)

    for ip_data in affect_data.ips:
        existing_ip = db.query(IP).filter(
            IP.adresse_ip == ip_data.adresse_ip
        ).first()

        if not existing_ip:
            logger.debug(f"Ajout d'une nouvelle IP : {ip_data.adresse_ip}")
            ip = IP(
                adresse_ip=ip_data.adresse_ip,
                affect_id=affect.id
            )
            db.add(ip)
            db.commit()
            db.refresh(ip)

            # Ajouter les ports
            for port_data in ip_data.ports:
                logger.debug(f"Ajout du port {port_data.numero}/{port_data.status} à l'IP {ip.adresse_ip}")
                port = Port(
                    numero=port_data.numero,
                    status=port_data.status,
                    ip_id=ip.id
                )
                db.add(port)
            db.commit()
            affect.ips.append(ip)
        else:
            logger.warning(f"IP déjà existante détectée : {existing_ip.adresse_ip}")
            affect.ips.append(existing_ip)

    affectationpath = generate_affect_pdf(affect)
    affect.affectationpath = affectationpath
    db.commit()

    logger.info(f"Affectation créée avec succès : ID={affect.id}")
    return affect

def get_affect(db: Session, affect_id: int):
    logger.info(f"Recherche de l'affectation avec ID: {affect_id}")
    affect = db.query(Affect).filter(Affect.id == affect_id).first()
    if affect:
        logger.info(f"Affectation trouvée: {affect.id}")
    else:
        logger.warning(f"Aucune affectation trouvée avec ID: {affect_id}")
    return affect

def list_affects(db: Session):
    logger.info("Récupération de toutes les affectations")
    affects = db.query(Affect).all()
    logger.info(f"{len(affects)} affectation(s) récupérée(s)")
    return affects

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
    logger.info(f"Tentative de suppression de l'auditeur ID {auditeur_id}")
    auditeur = db.query(Auditeur).filter(Auditeur.id == auditeur_id).first()
    if not auditeur:
        logger.warning(f"Auditeur ID {auditeur_id} non trouvé")
        return None

    for affect in auditeur.affects:
        affect.auditeurs.remove(auditeur)

    db.delete(auditeur)
    db.commit()
    logger.info(f"Auditeur ID {auditeur_id} supprimé")
    return auditeur

def update_auditeur(db: Session, auditeur_id: int, auditeur_data: AuditeurSchema):
    logger.info(f"Mise à jour de l'auditeur ID {auditeur_id}")
    auditeur = db.query(Auditeur).filter(Auditeur.id == auditeur_id).first()
    if not auditeur:
        logger.warning(f"Auditeur ID {auditeur_id} non trouvé pour mise à jour")
        return None

    auditeur.nom = auditeur_data.nom
    auditeur.prenom = auditeur_data.prenom
    auditeur.email = auditeur_data.email
    auditeur.phone = auditeur_data.phone
    auditeur.prestataire_id = auditeur_data.prestataire_id

    db.commit()
    db.refresh(auditeur)
    logger.info(f"Auditeur ID {auditeur_id} mis à jour")
    return auditeur
