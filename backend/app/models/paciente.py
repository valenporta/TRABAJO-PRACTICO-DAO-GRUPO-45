from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from ..core.db import Base

class Paciente(Base):
    __tablename__ = "pacientes"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    dni: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    apellido: Mapped[str] = mapped_column(String, nullable=False)
    fecha_nacimiento: Mapped[str] = mapped_column(String, nullable=False)  # ISO YYYY-MM-DD
    sexo: Mapped[str] = mapped_column(String, nullable=False)  # 'F'|'M'|'X'
    telefono: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    notas: Mapped[str | None] = mapped_column(Text, nullable=True)
    activo: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
