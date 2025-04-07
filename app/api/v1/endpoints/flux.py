from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.plan import create_flux, close_flux
from app.schemas.ip import FluxCreate, FluxResponse

router = APIRouter()

@router.post("/flux/", response_model=List[FluxResponse])
async def add_flux(flux_data: FluxCreate, db: Session = Depends(get_db)):
    return await create_flux(db, flux_data)

@router.put("/flux/{flux_id}/close", response_model=FluxResponse)
async def close_flux(flux_id: int, db: Session = Depends(get_db)):
    return await close_flux(db, flux_id)
