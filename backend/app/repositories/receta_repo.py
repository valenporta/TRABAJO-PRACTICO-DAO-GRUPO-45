from sqlalchemy.orm import Session
from ..models.receta import Receta

def create(db: Session, data: dict):
    obj = Receta(**data)
    db.add(obj)
    db.commit()
    db.refresh(obj)
    return obj

def get(db: Session, id: int):
    return db.query(Receta).get(id)
