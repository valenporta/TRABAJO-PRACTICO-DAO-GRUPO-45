from sqlalchemy.orm import Session
from sqlalchemy import and_, or_
from ..models.turno import Turno

def list_(db: Session, medico_id: int | None = None, paciente_id: int | None = None):
    q = db.query(Turno)
    if medico_id:
        q = q.filter(Turno.medico_id==medico_id)
    if paciente_id:
        q = q.filter(Turno.paciente_id==paciente_id)
    return q.order_by(Turno.fecha_hora).all()

def get(db: Session, id: int):
    return db.query(Turno).get(id)

def create(db: Session, data: dict):
    obj = Turno(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, id: int, data: dict):
    obj = get(db, id)
    if not obj:
        return None
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, id: int):
    obj = get(db, id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
