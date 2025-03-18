from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base

class Audit(Base):
    __tablename__ = "audits"

    id = Column(Integer, primary_key=True, index=True)
    date_creation = Column(Date, nullable=False)
    type_audit = Column(String(100), nullable=False)
    etat = Column(String(50), default="En attente")

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    requester = relationship("User", back_populates="audits")


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
