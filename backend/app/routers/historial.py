from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..schemas.historial import HistorialCreate, HistorialOut
from ..repositories import historial_repo as repo

router = APIRouter(prefix="/historial", tags=["historial"])

@router.get("/por-turno/{turno_id}", response_model=HistorialOut | None)
def get_by_turno(turno_id: int, db: Session = Depends(get_db)):
    return repo.get_by_turno(db, turno_id)

@router.post("/", response_model=HistorialOut, status_code=201)
def create(payload: HistorialCreate, db: Session = Depends(get_db)):
    # El 1:1 se garantiza por UNIQUE(turno_id)
    return repo.create(db, payload.dict())
