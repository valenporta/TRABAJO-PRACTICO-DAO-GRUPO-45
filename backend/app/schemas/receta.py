from typing import Optional
from .common import ORMSchema

class RecetaCreate(ORMSchema):
    fecha: str
    medico_id: int
    paciente_id: int
    turno_id: Optional[int] = None
    contenido: str
    observaciones: Optional[str] = None

class RecetaOut(RecetaCreate):
    id: int
    numero: int | None = None
