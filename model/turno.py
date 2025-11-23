
class Turno:
    def __init__(
        self,
        id_paciente,
        id_medico,
        fecha,
        hora,
        id_estado=1,
        motivo=None,
        id_turno=None,
        paciente_nombre=None,
        medico_nombre=None,
        estado_nombre=None,
    ):
        self.id_turno = id_turno
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.fecha = fecha        # "2024-11-21"
        self.hora = hora          # "10:00"
        self.id_estado = id_estado
        self.motivo = motivo
        self.paciente_nombre = paciente_nombre
        self.medico_nombre = medico_nombre
        self.estado_nombre = estado_nombre

    def __str__(self):
        return (
            f"Turno {self.fecha} {self.hora} - Medico {self.id_medico}, "
            f"Paciente {self.id_paciente}"
        )
