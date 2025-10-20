from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from sqlalchemy import and_
from ..models.turno import Turno
from ..services.agenda_service import within_agenda

ALLOWED = {
    "reservado": {"confirmado","cancelado"},
    "confirmado": {"atendido","ausente","cancelado"},
    "atendido": set(),
    "ausente": set(),
    "cancelado": set(),
}

def _dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M")

def _overlaps(a_start, a_end, b_start, b_end) -> bool:
    return a_start < b_end and b_start < a_end

def validate_and_create(db: Session, data: dict):
    # Agenda
    if not within_agenda(db, data["medico_id"], data["fecha_hora"], data.get("duracion_min", 30)):
        raise ValueError("fuera_de_agenda")
    # Solapamiento
    start = _dt(data["fecha_hora"])
    end = start + timedelta(minutes=data.get("duracion_min", 30))
    mismos = db.query(Turno).filter(Turno.medico_id==data["medico_id"]).all()
    for t in mismos:
        ts = _dt(t.fecha_hora)
        te = ts + timedelta(minutes=t.duracion_min)
        if _overlaps(start, end, ts, te):
            raise ValueError("solapado")
    # OK
    return True

def change_state(db: Session, turno: Turno, new_state: str):
    cur = turno.estado
    if new_state not in ALLOWED.get(cur, set()):
        raise ValueError("transicion_invalida")
    turno.estado = new_state
    db.commit()
    db.refresh(turno)
    return turno
