class Medico:
    def __init__(self, dni, nombre, apellido, matricula, telefono=None, id_medico=None, especialidades=None):
        self.id_medico = id_medico
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.matricula = matricula
        self.telefono = telefono
        self.especialidades = especialidades

    def __str__(self):
        return f"Dr. {self.apellido}, {self.nombre} (Matrícula: {self.matricula})"