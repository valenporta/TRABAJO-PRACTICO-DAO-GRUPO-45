from typing import Optional
from .common import ORMSchema

class HistorialCreate(ORMSchema):
    turno_id: int
    paciente_id: int
    medico_id: int
    fecha: str  # YYYY-MM-DD
    motivo: str
    diagnostico: str
    indicaciones: Optional[str] = None

class HistorialOut(HistorialCreate):
    id: int
