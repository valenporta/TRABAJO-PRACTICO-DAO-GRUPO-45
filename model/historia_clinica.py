
class HistoriaClinica:
    def __init__(
        self,
        id_paciente,
        fecha,
        resumen,
        id_atencion=None,
        id_historia=None,
        diagnostico=None,
        procedimiento=None,
        indicaciones=None,
        medico_nombre=None,
        paciente_nombre=None,
        turno_fecha=None,
        turno_hora=None,
    ):
        self.id_historia = id_historia
        self.id_paciente = id_paciente
        self.fecha = fecha
        self.resumen = resumen
        self.id_atencion = id_atencion
        self.diagnostico = diagnostico
        self.procedimiento = procedimiento
        self.indicaciones = indicaciones
        self.medico_nombre = medico_nombre
        self.paciente_nombre = paciente_nombre
        self.turno_fecha = turno_fecha
        self.turno_hora = turno_hora

    def __str__(self):
        return f"Historia clinica de paciente {self.id_paciente} - {self.fecha}"
