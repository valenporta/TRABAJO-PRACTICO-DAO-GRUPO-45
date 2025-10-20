from sqlalchemy.orm import Session
from ..models.agenda import AgendaSemanal

def list_by_medico(db: Session, medico_id: int):
    return db.query(AgendaSemanal).filter(AgendaSemanal.medico_id==medico_id).order_by(AgendaSemanal.dia_semana).all()

def create(db: Session, data: dict):
    obj = AgendaSemanal(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def update(db: Session, id: int, data: dict):
    obj = db.query(AgendaSemanal).get(id)
    if not obj:
        return None
    for k, v in data.items():
        setattr(obj, k, v)
    db.commit()
    db.refresh(obj)
    return obj

def delete(db: Session, id: int):
    obj = db.query(AgendaSemanal).get(id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True
