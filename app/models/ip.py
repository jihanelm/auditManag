from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from app.core.database import Base
from app.models.associations import affect_ip

class IP(Base):
    __tablename__ = "ips"

    id = Column(Integer, primary_key=True, index=True)
    affect_id = Column(Integer, ForeignKey("affects.id"), nullable=False)
    adresse_ip = Column(String(50), nullable=False)

    affect = relationship("Affect", secondary=affect_ip, back_populates="ips")
    ports = relationship("Port", back_populates="ip", cascade="all, delete-orphan")