
class Especialidad:
    def __init__(self, nombre, id_especialidad=None):
        self.id_especialidad = id_especialidad
        self.nombre = nombre

    def __str__(self):
        return self.nombre