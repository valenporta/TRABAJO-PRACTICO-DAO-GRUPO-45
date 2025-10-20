from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey, Text
from ..core.db import Base

class Receta(Base):
    __tablename__ = "recetas"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    numero: Mapped[int | None] = mapped_column(Integer, unique=True, nullable=True)  # trigger lo iguala a id si NULL
    fecha: Mapped[str] = mapped_column(String, nullable=False)  # 'YYYY-MM-DD'
    medico_id: Mapped[int] = mapped_column(ForeignKey("medicos.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    turno_id: Mapped[int | None] = mapped_column(ForeignKey("turnos.id", ondelete="SET NULL", onupdate="CASCADE"), nullable=True)
    contenido: Mapped[str] = mapped_column(Text, nullable=False)
    observaciones: Mapped[str | None] = mapped_column(Text, nullable=True)
