from datetime import datetime, timedelta
from services.agenda_service import AgendaService
from model.agenda import Agenda

class AgendaController:

    def __init__(self):
        self.service = AgendaService()

    def crear_agenda(self, datos: dict):
        if "id_medico" not in datos or "dia_semana" not in datos:
            raise ValueError("Faltan datos obligatorios.")
        
        if not datos.get("hora_desde"):
            raise ValueError("Debe especificar hora de inicio.")

        try:
            duracion_horas = float(datos.get("duracion_horas", 0))
            if duracion_horas <= 0:
                raise ValueError("La duración debe ser mayor a 0.")
            
            formato = "%H:%M"
            inicio_dt = datetime.strptime(datos["hora_desde"], formato)
            
            fin_dt = inicio_dt + timedelta(hours=duracion_horas)
            
            hora_hasta_calc = fin_dt.strftime(formato)

        except ValueError as e:
            raise ValueError(f"Error en los datos de tiempo: {str(e)}")

        # 2. Validar solapamiento 
        solapamiento = self.service.verificar_solapamiento(
            datos["id_medico"], 
            datos["dia_semana"], 
            datos["hora_desde"], 
            hora_hasta_calc
        )
        
        if solapamiento:
            raise ValueError(f"El médico ya tiene agenda de {datos['hora_desde']} a {hora_hasta_calc}. Elija otro horario.")

        # 3. Crear objeto
        nueva_agenda = Agenda(
            id_medico=datos["id_medico"],
            dia_semana=datos["dia_semana"],
            hora_desde=datos["hora_desde"],
            hora_hasta=hora_hasta_calc, 
            duracion_turno_min=datos.get("duracion_turno_min", 30)
        )
        
        return self.service.crear(nueva_agenda)

    def obtener_agendas_medico(self, id_medico):
        if not id_medico:
             raise ValueError("El ID del médico es obligatorio.")
        return self.service.obtener_por_medico(id_medico)
    
    # Eliminar Agenda
    def eliminar_agenda(self, id_agenda):
        self.service.eliminar(id_agenda)