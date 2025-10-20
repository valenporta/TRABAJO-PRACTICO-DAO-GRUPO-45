from typing import Optional
from .common import ORMSchema

class TurnoBase(ORMSchema):
    medico_id: int
    paciente_id: int
    fecha_hora: str  # 'YYYY-MM-DD HH:MM'
    duracion_min: int = 30
    estado: str = "reservado"
    especialidad_id: Optional[int] = None  # opcional

class TurnoCreate(TurnoBase):
    pass

class TurnoUpdate(ORMSchema):
    fecha_hora: Optional[str] = None
    duracion_min: Optional[int] = None
    estado: Optional[str] = None
    especialidad_id: Optional[int] = None

class TurnoOut(TurnoBase):
    id: int
