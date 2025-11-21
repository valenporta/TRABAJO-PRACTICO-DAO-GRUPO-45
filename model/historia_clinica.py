
class HistoriaClinica:
    def __init__(self, id_paciente, fecha, resumen, id_atencion=None, id_historia=None):
        self.id_historia = id_historia
        self.id_paciente = id_paciente
        self.fecha = fecha
        self.resumen = resumen
        self.id_atencion = id_atencion

    def __str__(self):
        return f"Historia clínica de paciente {self.id_paciente} - {self.fecha}"
