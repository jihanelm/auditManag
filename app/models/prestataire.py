from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.core.database import Base

class Prestataire(Base):
    __tablename__ = "prestataires"

    id = Column(Integer, primary_key=True, index=True)
    nom = Column(String(100), nullable=False, unique=True)

    auditeurs = relationship("Auditeur", back_populates="prestataire")
    affects = relationship("Affect", back_populates="prestataire")