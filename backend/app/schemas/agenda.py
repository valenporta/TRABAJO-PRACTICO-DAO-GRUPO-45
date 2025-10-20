from typing import Optional
from .common import ORMSchema

class AgendaBase(ORMSchema):
    medico_id: int
    dia_semana: int  # 0..6
    hora_inicio: str
    hora_fin: str
    activo: int = 1

class AgendaCreate(AgendaBase):
    pass

class AgendaUpdate(ORMSchema):
    dia_semana: Optional[int] = None
    hora_inicio: Optional[str] = None
    hora_fin: Optional[str] = None
    activo: Optional[int] = None

class AgendaOut(AgendaBase):
    id: int
