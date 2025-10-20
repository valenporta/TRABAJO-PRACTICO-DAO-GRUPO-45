from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, Text
from ..core.db import Base

class Especialidad(Base):
    __tablename__ = "especialidades"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    nombre: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text, nullable=True)
    activa: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
