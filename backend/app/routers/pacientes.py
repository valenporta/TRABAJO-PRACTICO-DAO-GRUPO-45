from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..schemas.paciente import PacienteCreate, PacienteUpdate, PacienteOut
from ..repositories import paciente_repo as repo

router = APIRouter(prefix="/pacientes", tags=["pacientes"])

@router.get("/", response_model=list[PacienteOut])
def list_(db: Session = Depends(get_db)):
    return repo.list_(db)

@router.post("/", response_model=PacienteOut, status_code=201)
def create(payload: PacienteCreate, db: Session = Depends(get_db)):
    return repo.create(db, payload.dict())

@router.get("/{id}", response_model=PacienteOut)
def get(id: int, db: Session = Depends(get_db)):
    obj = repo.get(db, id)
    if not obj:
        raise HTTPException(404, "Paciente no encontrado")
    return obj

@router.put("/{id}", response_model=PacienteOut)
def update(id: int, payload: PacienteUpdate, db: Session = Depends(get_db)):
    obj = repo.update(db, id, {k:v for k,v in payload.dict().items() if v is not None})
    if not obj:
        raise HTTPException(404, "Paciente no encontrado")
    return obj

@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    ok = repo.delete(db, id)
    if not ok:
        raise HTTPException(404, "Paciente no encontrado")
    return
