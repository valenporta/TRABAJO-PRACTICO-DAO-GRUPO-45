from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..schemas.medico import MedicoCreate, MedicoUpdate, MedicoOut, MedicoEspecialidadAssign
from ..repositories import medico_repo as repo

router = APIRouter(prefix="/medicos", tags=["medicos"])

@router.get("/", response_model=list[MedicoOut])
def list_(db: Session = Depends(get_db)):
    return repo.list_(db)

@router.post("/", response_model=MedicoOut, status_code=201)
def create(payload: MedicoCreate, db: Session = Depends(get_db)):
    return repo.create(db, payload.dict())

@router.get("/{id}", response_model=MedicoOut)
def get(id: int, db: Session = Depends(get_db)):
    obj = repo.get(db, id)
    if not obj:
        raise HTTPException(404, "Médico no encontrado")
    return obj

@router.put("/{id}", response_model=MedicoOut)
def update(id: int, payload: MedicoUpdate, db: Session = Depends(get_db)):
    obj = repo.update(db, id, {k:v for k,v in payload.dict().items() if v is not None})
    if not obj:
        raise HTTPException(404, "Médico no encontrado")
    return obj

@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    ok = repo.delete_(db, id)
    if not ok:
        raise HTTPException(404, "Médico no encontrado")
    return

@router.post("/{id}/especialidades", status_code=204)
def add_especialidad(id: int, payload: MedicoEspecialidadAssign, db: Session = Depends(get_db)):
    repo.add_especialidad(db, id, payload.especialidad_id)
    return

@router.delete("/{id}/especialidades/{especialidad_id}", status_code=204)
def remove_especialidad(id: int, especialidad_id: int, db: Session = Depends(get_db)):
    repo.remove_especialidad(db, id, especialidad_id)
    return
