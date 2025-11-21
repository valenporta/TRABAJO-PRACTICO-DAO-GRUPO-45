
class Agenda:
    def __init__(self, id_medico, dia_semana, hora_desde, hora_hasta, duracion_turno_min, id_agenda=None):
        self.id_agenda = id_agenda
        self.id_medico = id_medico
        self.dia_semana = dia_semana      # 0=lunes ... 6=domingo
        self.hora_desde = hora_desde      # "08:00"
        self.hora_hasta = hora_hasta      # "12:00"
        self.duracion_turno_min = duracion_turno_min

    def __str__(self):
        return f"Día {self.dia_semana} - {self.hora_desde}-{self.hora_hasta}"
