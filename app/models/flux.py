from sqlalchemy import Column, Integer, String, Boolean, DateTime
from sqlalchemy.orm import declarative_base
import datetime

Base = declarative_base()

class Flux(Base):
    __tablename__ = "flux"

    id = Column(Integer, primary_key=True, index=True)
    ip = Column(String, nullable=False)
    port = Column(Integer, nullable=False)
    status = Column(Boolean, default=True)  # True = ouvert, False = fermé
    created_at = Column(DateTime, default=datetime.datetime.utcnow)
