from typing import Optional, List
from pydantic import EmailStr
from .common import ORMSchema

class MedicoBase(ORMSchema):
    matricula: str
    nombre: str
    apellido: str
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    activo: int = 1

class MedicoCreate(MedicoBase):
    pass

class MedicoUpdate(ORMSchema):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    activo: Optional[int] = None

class MedicoOut(MedicoBase):
    id: int

class MedicoEspecialidadAssign(ORMSchema):
    especialidad_id: int
