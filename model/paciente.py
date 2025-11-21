class Paciente:
    def __init__(self, dni, nombre, apellido, telefono=None, email=None, fecha_nac=None, id_paciente=None):
        self.id_paciente = id_paciente
        self.dni = dni
        self.nombre = nombre
        self.apellido = apellido
        self.telefono = telefono
        self.email = email
        self.fecha_nac = fecha_nac

    def __str__(self):
        return f"{self.apellido}, {self.nombre} (DNI: {self.dni})"