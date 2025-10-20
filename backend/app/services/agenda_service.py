from datetime import datetime, time, timedelta
from sqlalchemy.orm import Session
from ..models.agenda import AgendaSemanal

def _parse_hhmm(h: str) -> time:
    return datetime.strptime(h, "%H:%M").time()

def _dt(s: str) -> datetime:
    return datetime.strptime(s, "%Y-%m-%d %H:%M")

def within_agenda(db: Session, medico_id: int, fecha_hora: str, duracion_min: int) -> bool:
    dt = _dt(fecha_hora)
    dow = (dt.weekday())  # 0 lunes
    rows = db.query(AgendaSemanal).filter(
        AgendaSemanal.medico_id==medico_id,
        AgendaSemanal.dia_semana==dow,
        AgendaSemanal.activo==1
    ).all()
    if not rows:
        return False
    start = dt.time()
    end = (dt + timedelta(minutes=duracion_min)).time()
    for r in rows:
        si = _parse_hhmm(r.hora_inicio)
        sf = _parse_hhmm(r.hora_fin)
        if si <= start and end <= sf:
            return True
    return False
