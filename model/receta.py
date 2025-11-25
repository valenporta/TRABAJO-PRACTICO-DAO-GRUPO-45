
class Receta:
    def __init__(self, id_atencion, fecha, detalle, id_receta=None, diagnostico=None):
        self.id_receta = id_receta
        self.id_atencion = id_atencion
        self.fecha = fecha
        self.detalle = detalle
        self.diagnostico = diagnostico

    def __str__(self):
        return f"Receta {self.fecha}: {self.detalle[:20]}..."
