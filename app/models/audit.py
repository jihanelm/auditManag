from sqlalchemy import Column, Integer, String, Date
from sqlalchemy.orm import relationship
from app.core.database import Base
from datetime import date

class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    date_creation = Column(Date, default=date.today, nullable=False)
    type_audit = Column(String(100), nullable=False)
    etat = Column(String(50), default="En attente")

    demandeur_nom = Column(String(100), nullable=False)
    demandeur_prenom = Column(String(100), nullable=False)
    demandeur_email = Column(String(255), nullable=False)
    demandeur_phone = Column(String(20), nullable=False)
    demandeur_departement = Column(String(100), nullable=False)
    description = Column(String(500), nullable=False)
    objectif = Column(String(500), nullable=False)
    urgence = Column(String(50), nullable=False)
    domain_name = Column(String(100), nullable=False)
    fichier_attache = Column(String(255), nullable=True)
    pdf_report_path = Column(String(255), nullable=True)

    affects = relationship("Affect", back_populates="audit")
    plans = relationship("Plan", back_populates="audit")

    def __repr__(self):
        return f"<Audit(id={self.id}, etat={self.etat})>"
