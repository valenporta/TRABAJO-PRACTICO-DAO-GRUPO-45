from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..schemas.especialidad import EspecialidadCreate, EspecialidadUpdate, EspecialidadOut
from ..repositories import especialidad_repo as repo

router = APIRouter(prefix="/especialidades", tags=["especialidades"])

@router.get("/", response_model=list[EspecialidadOut])
def list_(db: Session = Depends(get_db)):
    return repo.list_(db)

@router.post("/", response_model=EspecialidadOut, status_code=201)
def create(payload: EspecialidadCreate, db: Session = Depends(get_db)):
    return repo.create(db, payload.dict())

@router.put("/{id}", response_model=EspecialidadOut)
def update(id: int, payload: EspecialidadUpdate, db: Session = Depends(get_db)):
    obj = repo.update(db, id, {k:v for k,v in payload.dict().items() if v is not None})
    if not obj:
        raise HTTPException(404, "Especialidad no encontrada")
    return obj

@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    ok = repo.delete(db, id)
    if not ok:
        raise HTTPException(404, "Especialidad no encontrada")
    return
