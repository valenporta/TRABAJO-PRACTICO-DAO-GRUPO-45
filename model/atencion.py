
class Atencion:
    def __init__(
        self,
        id_turno,
        diagnostico=None,
        procedimiento=None,
        indicaciones=None,
        id_atencion=None,
        turno_fecha=None,
        turno_hora=None,
        medico_nombre=None,
        paciente_nombre=None,
    ):
        self.id_atencion = id_atencion
        self.id_turno = id_turno
        self.diagnostico = diagnostico
        self.procedimiento = procedimiento
        self.indicaciones = indicaciones
        self.turno_fecha = turno_fecha
        self.turno_hora = turno_hora
        self.medico_nombre = medico_nombre
        self.paciente_nombre = paciente_nombre

    def __str__(self):
        return f"Atencion del turno {self.id_turno}"
