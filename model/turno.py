
class Turno:
    def __init__(self, id_paciente, id_medico, fecha, hora, id_estado=1, motivo=None, id_turno=None):
        self.id_turno = id_turno
        self.id_paciente = id_paciente
        self.id_medico = id_medico
        self.fecha = fecha        # "2024-11-21"
        self.hora = hora          # "10:00"
        self.id_estado = id_estado
        self.motivo = motivo

    def __str__(self):
        return f"Turno {self.fecha} {self.hora} - Medico {self.id_medico}, Paciente {self.id_paciente}"
