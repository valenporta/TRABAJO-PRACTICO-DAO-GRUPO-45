from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String
from ..core.db import Base

class Medico(Base):
    __tablename__ = "medicos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    matricula: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    nombre: Mapped[str] = mapped_column(String, nullable=False)
    apellido: Mapped[str] = mapped_column(String, nullable=False)
    telefono: Mapped[str | None] = mapped_column(String, nullable=True)
    email: Mapped[str | None] = mapped_column(String, nullable=True)
    activo: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
