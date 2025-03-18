from sqlalchemy import Column, Integer, String, Date, ForeignKey
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
    fichier_attache = Column(String(255), nullable=True)  # Stocke le chemin du fichier

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    requester = relationship("User", back_populates="audits")

    def __repr__(self):
        return f"<Audit(id={self.id}, type_audit={self.type_audit}, etat={self.etat})>"


    """
    auditorIn_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    auditorEx_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    prestataire_id = Column(Integer, ForeignKey("prestataires.id"), nullable=False)
    flux_id = Column(Integer, ForeignKey("flux.id"), nullable=False)

    auditor_in = relationship("User", foreign_keys=[auditorIn_id])
    auditor_ex = relationship("User", foreign_keys=[auditorEx_id])
    prestataire = relationship("Prestataire")
    flux = relationship("Flux")
    
    """
