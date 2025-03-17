from sqlalchemy import Column, Integer, String, Date, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base


class Plan(Base):
    __tablename__ = "plans"

    id = Column(Integer, primary_key=True, index=True)
    ref = Column(String(50), unique=True, index=True)
    type_audit = Column(String(100))
    date_debut = Column(Date)
    date_realisation = Column(Date)
    duree = Column(Integer)  # En jours
    date_fin = Column(Date)
    status = Column(String(50))
    remarques = Column(String(255))

    audit_id = Column(Integer, ForeignKey("audits.id"))
    audit = relationship("Audit")
