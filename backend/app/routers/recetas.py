from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..schemas.receta import RecetaCreate, RecetaOut
from ..repositories import receta_repo as repo

router = APIRouter(prefix="/recetas", tags=["recetas"])

@router.post("/", response_model=RecetaOut, status_code=201)
def create(payload: RecetaCreate, db: Session = Depends(get_db)):
    obj = repo.create(db, payload.dict())
    return obj

@router.get("/{id}", response_model=RecetaOut)
def get(id: int, db: Session = Depends(get_db)):
    obj = repo.get(db, id)
    if not obj:
        raise HTTPException(404, "Receta no encontrada")
    return obj
