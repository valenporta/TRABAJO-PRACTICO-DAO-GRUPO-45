from sqlalchemy.orm import Session
from ..models.especialidad import Especialidad

def list_(db: Session):
    return db.query(Especialidad).order_by(Especialidad.nombre).all()

def get(db: Session, id: int):
    return db.query(Especialidad).get(id)

def create(db: Session, data: dict):
    obj = Especialidad(**data)
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
