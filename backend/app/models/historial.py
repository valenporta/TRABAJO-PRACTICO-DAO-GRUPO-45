from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from ..core.db import Base

class HistorialClinico(Base):
    __tablename__ = "historial_clinico"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    turno_id: Mapped[int] = mapped_column(ForeignKey("turnos.id", ondelete="RESTRICT", onupdate="CASCADE"), unique=True, nullable=False)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    medico_id: Mapped[int] = mapped_column(ForeignKey("medicos.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    fecha: Mapped[str] = mapped_column(String, nullable=False)  # 'YYYY-MM-DD'
    motivo: Mapped[str] = mapped_column(String, nullable=False)
    diagnostico: Mapped[str] = mapped_column(String, nullable=False)
    indicaciones: Mapped[str | None] = mapped_column(String, nullable=True)
