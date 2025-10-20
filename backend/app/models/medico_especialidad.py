from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import Integer, ForeignKey
from ..core.db import Base

class MedicoEspecialidad(Base):
    __tablename__ = "medico_especialidad"
    medico_id: Mapped[int] = mapped_column(ForeignKey("medicos.id", ondelete="RESTRICT", onupdate="CASCADE"), primary_key=True)
    especialidad_id: Mapped[int] = mapped_column(ForeignKey("especialidades.id", ondelete="RESTRICT", onupdate="CASCADE"), primary_key=True)
