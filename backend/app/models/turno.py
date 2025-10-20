from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from ..core.db import Base

class Turno(Base):
    __tablename__ = "turnos"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    medico_id: Mapped[int] = mapped_column(ForeignKey("medicos.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    paciente_id: Mapped[int] = mapped_column(ForeignKey("pacientes.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    fecha_hora: Mapped[str] = mapped_column(String, nullable=False)  # 'YYYY-MM-DD HH:MM'
    duracion_min: Mapped[int] = mapped_column(Integer, nullable=False, default=30)
    estado: Mapped[str] = mapped_column(String, nullable=False, default="reservado")  # reservado, confirmado, atendido, ausente, cancelado
    recordatorio_24h_enviado: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    recordatorio_2h_enviado: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    created_at: Mapped[str] = mapped_column(String, nullable=False, default="")  # DB trigger set
    updated_at: Mapped[str] = mapped_column(String, nullable=False, default="")
    # Opcional si ejecutaste el ALTER:
    especialidad_id: Mapped[int | None] = mapped_column(ForeignKey("especialidades.id"), nullable=True)
