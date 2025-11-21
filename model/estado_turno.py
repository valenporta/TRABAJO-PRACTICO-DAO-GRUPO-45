
class EstadoTurno:
    def __init__(self, nombre, id_estado=None):
        self.id_estado = id_estado
        self.nombre = nombre

    def __str__(self):
        return self.nombre