from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, String, ForeignKey
from ..core.db import Base

class AgendaSemanal(Base):
    __tablename__ = "agenda_semanal"
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    medico_id: Mapped[int] = mapped_column(ForeignKey("medicos.id", ondelete="RESTRICT", onupdate="CASCADE"), nullable=False)
    dia_semana: Mapped[int] = mapped_column(Integer, nullable=False)  # 0..6
    hora_inicio: Mapped[str] = mapped_column(String, nullable=False)  # 'HH:MM'
    hora_fin: Mapped[str] = mapped_column(String, nullable=False)     # 'HH:MM'
    activo: Mapped[int] = mapped_column(Integer, nullable=False, default=1)
