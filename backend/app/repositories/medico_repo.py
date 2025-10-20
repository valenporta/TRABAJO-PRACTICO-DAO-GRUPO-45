from sqlalchemy.orm import Session
from sqlalchemy import select, insert, delete
from ..models.medico import Medico
from ..models.medico_especialidad import MedicoEspecialidad

def list_(db: Session):
    return db.query(Medico).order_by(Medico.apellido, Medico.nombre).all()

def get(db: Session, id: int):
    return db.query(Medico).get(id)

def create(db: Session, data: dict):
    obj = Medico(**data)
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

def delete_(db: Session, id: int):
    obj = get(db, id)
    if not obj:
        return False
    db.delete(obj)
    db.commit()
    return True

def add_especialidad(db: Session, medico_id: int, especialidad_id: int):
    db.execute(insert(MedicoEspecialidad).values(medico_id=medico_id, especialidad_id=especialidad_id))
    db.commit()

def remove_especialidad(db: Session, medico_id: int, especialidad_id: int):
    db.execute(delete(MedicoEspecialidad).where(
        MedicoEspecialidad.medico_id==medico_id,
        MedicoEspecialidad.especialidad_id==especialidad_id
    ))
    db.commit()
