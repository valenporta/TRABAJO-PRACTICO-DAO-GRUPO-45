from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..schemas.agenda import AgendaCreate, AgendaUpdate, AgendaOut
from ..repositories import agenda_repo as repo

router = APIRouter(prefix="/agenda", tags=["agenda"])

@router.get("/{medico_id}", response_model=list[AgendaOut])
def list_by_medico(medico_id: int, db: Session = Depends(get_db)):
    return repo.list_by_medico(db, medico_id)

@router.post("/", response_model=AgendaOut, status_code=201)
def create(payload: AgendaCreate, db: Session = Depends(get_db)):
    return repo.create(db, payload.dict())

@router.put("/{id}", response_model=AgendaOut)
def update(id: int, payload: AgendaUpdate, db: Session = Depends(get_db)):
    obj = repo.update(db, id, {k:v for k,v in payload.dict().items() if v is not None})
    if not obj:
        raise HTTPException(404, "Agenda no encontrada")
    return obj

@router.delete("/{id}", status_code=204)
def delete(id: int, db: Session = Depends(get_db)):
    ok = repo.delete(db, id)
    if not ok:
        raise HTTPException(404, "Agenda no encontrada")
    return
