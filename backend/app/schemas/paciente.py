from pydantic import Field, EmailStr
from typing import Optional
from .common import ORMSchema

class PacienteBase(ORMSchema):
    dni: str
    nombre: str
    apellido: str
    fecha_nacimiento: str  # YYYY-MM-DD
    sexo: str = Field(pattern="^(F|M|X)$")
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    notas: Optional[str] = None
    activo: int = 1

class PacienteCreate(PacienteBase):
    pass

class PacienteUpdate(ORMSchema):
    nombre: Optional[str] = None
    apellido: Optional[str] = None
    fecha_nacimiento: Optional[str] = None
    sexo: Optional[str] = None
    telefono: Optional[str] = None
    email: Optional[EmailStr] = None
    notas: Optional[str] = None
    activo: Optional[int] = None

class PacienteOut(PacienteBase):
    id: int
