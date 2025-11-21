
class Atencion:
    def __init__(self, id_turno, diagnostico=None, procedimiento=None, indicaciones=None, id_atencion=None):
        self.id_atencion = id_atencion
        self.id_turno = id_turno
        self.diagnostico = diagnostico
        self.procedimiento = procedimiento
        self.indicaciones = indicaciones

    def __str__(self):
        return f"Atención del turno {self.id_turno}"
