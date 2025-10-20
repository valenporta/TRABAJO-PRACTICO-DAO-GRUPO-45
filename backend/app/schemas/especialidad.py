from typing import Optional
from .common import ORMSchema

class EspecialidadBase(ORMSchema):
    nombre: str
    descripcion: Optional[str] = None
    activa: int = 1

class EspecialidadCreate(EspecialidadBase):
    pass

class EspecialidadUpdate(ORMSchema):
    nombre: Optional[str] = None
    descripcion: Optional[str] = None
    activa: Optional[int] = None

class EspecialidadOut(EspecialidadBase):
    id: int
