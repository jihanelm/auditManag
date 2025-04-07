from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.associations import affect_auditeur, affect_ip
from datetime import date

class Affect(Base):
    __tablename__ = "affects"

    id = Column(Integer, primary_key=True, index=True)
    audit_id = Column(Integer, ForeignKey("audits.id"), nullable=False)
    date_affectation = Column(Date, default=date.today, nullable=False)
    affectationpath = Column(String(255), nullable=True)
    prestataire_id = Column(Integer, ForeignKey("prestataires.id"))

    audit = relationship("Audit", back_populates="affects")
    auditeurs = relationship("Auditeur", secondary=affect_auditeur, back_populates="affects")
    prestataire = relationship("Prestataire", back_populates="affects")
    ips = relationship("IP", secondary=affect_ip, back_populates="affect")