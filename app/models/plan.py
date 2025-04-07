from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    ref = Column(String(50), unique=True, index=True)
    type_audit = Column(String(100), nullable=False)
    date_debut = Column(Date, nullable=False)
    date_realisation = Column(Date, nullable=True)
    duree = Column(Integer, nullable=False)  # En jours
    date_fin = Column(Date, nullable=False)
    status = Column(String(50), nullable=False)
    remarques = Column(String(255), nullable=True)

    audit_id = Column(Integer, ForeignKey("audits.id"), nullable=True)
    audit = relationship("Audit", back_populates="plans")