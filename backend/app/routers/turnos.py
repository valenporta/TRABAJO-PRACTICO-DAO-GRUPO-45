from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..schemas.turno import TurnoCreate, TurnoUpdate, TurnoOut
from ..repositories import turno_repo as repo
from ..services.turnos_service import validate_and_create, change_state

router = APIRouter(prefix="/turnos", tags=["turnos"])

@router.get("/", response_model=list[TurnoOut])
def list_(medico_id: int | None = None, paciente_id: int | None = None, db: Session = Depends(get_db)):
    return repo.list_(db, medico_id, paciente_id)

@router.post("/", response_model=TurnoOut, status_code=201)
def create(payload: TurnoCreate, db: Session = Depends(get_db)):
    try:
        validate_and_create(db, payload.dict())
    except ValueError as e:
        msg = str(e)
        if msg == "fuera_de_agenda":
            raise HTTPException(400, "Turno fuera de agenda semanal del médico")
        if msg == "solapado":
            raise HTTPException(400, "Turno solapado con otro existente")
        raise
    return repo.create(db, payload.dict())

@router.put("/{id}", response_model=TurnoOut)
def update(id: int, payload: TurnoUpdate, db: Session = Depends(get_db)):
    obj = repo.update(db, id, {k:v for k,v in payload.dict().items() if v is not None})
    if not obj:
        raise HTTPException(404, "Turno no encontrado")
    return obj

@router.post("/{id}/confirmar", response_model=TurnoOut)
def confirmar(id: int, db: Session = Depends(get_db)):
    obj = repo.get(db, id)
    if not obj:
        raise HTTPException(404, "Turno no encontrado")
    return change_state(db, obj, "confirmado")

@router.post("/{id}/cancelar", response_model=TurnoOut)
def cancelar(id: int, db: Session = Depends(get_db)):
    obj = repo.get(db, id)
    if not obj:
        raise HTTPException(404, "Turno no encontrado")
    return change_state(db, obj, "cancelado")

@router.post("/{id}/atendido", response_model=TurnoOut)
def atendido(id: int, db: Session = Depends(get_db)):
    obj = repo.get(db, id)
    if not obj:
        raise HTTPException(404, "Turno no encontrado")
    return change_state(db, obj, "atendido")

@router.post("/{id}/ausente", response_model=TurnoOut)
def ausente(id: int, db: Session = Depends(get_db)):
    obj = repo.get(db, id)
    if not obj:
        raise HTTPException(404, "Turno no encontrado")
    return change_state(db, obj, "ausente")

@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    ok = repo.delete(db, id)
    if not ok:
        raise HTTPException(404, "Turno no encontrado")
    return
