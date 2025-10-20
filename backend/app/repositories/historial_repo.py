from sqlalchemy.orm import Session
from ..models.historial import HistorialClinico

def get_by_turno(db: Session, turno_id: int):
    return db.query(HistorialClinico).filter(HistorialClinico.turno_id==turno_id).first()

def create(db: Session, data: dict):
    obj = HistorialClinico(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj
