from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from ..core.db import get_db
from ..services import reportes_service as svc

router = APIRouter(prefix="/reportes", tags=["reportes"])

@router.get("/turnos-por-medico")
def turnos_por_medico(medico_id: int, desde: str, hasta: str, db: Session = Depends(get_db)):
    return svc.turnos_por_medico(db, medico_id, desde, hasta)

@router.get("/turnos-por-especialidad")
def turnos_por_especialidad(desde: str, hasta: str, db: Session = Depends(get_db)):
    return svc.turnos_por_especialidad(db, desde, hasta)

@router.get("/pacientes-atendidos")
def pacientes_atendidos(desde: str, hasta: str, db: Session = Depends(get_db)):
    return svc.pacientes_atendidos(db, desde, hasta)

@router.get("/asistencia-vs-inasistencias")
def asistencia_vs_inasistencias(desde: str, hasta: str, db: Session = Depends(get_db)):
    return svc.asistencia_vs_inasistencias(db, desde, hasta)
