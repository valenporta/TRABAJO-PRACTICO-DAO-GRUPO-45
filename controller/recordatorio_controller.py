from datetime import datetime, timedelta
from services.turno_service import TurnoService
from services.email_service import EmailService

class RecordatorioController:
    def __init__(self):
        self.turno_service = TurnoService()
        self.email_service = EmailService()

    def enviar_recordatorios_manana(self):
        # Calcular fecha de mañana
        manana = datetime.now() + timedelta(days=1)
        fecha_manana = manana.strftime("%Y-%m-%d")
        
        # Obtener turnos
        turnos = self.turno_service.obtener_turnos_por_fecha(fecha_manana)
        
        enviados = 0
        errores = 0
        
        print(f"--- Procesando recordatorios para {fecha_manana} ---")
        
        for turno in turnos:
            if hasattr(turno, 'email_paciente') and turno.email_paciente:
                asunto = "Recordatorio de Turno - Clínica"
                cuerpo = f"""
                Hola {turno.paciente_nombre},
                
                Le recordamos que tiene un turno agendado para mañana:
                
                Fecha: {turno.fecha}
                Hora: {turno.hora}
                Médico: {turno.medico_nombre}
                Motivo: {turno.motivo}
                
                Por favor, recuerde asistir puntual.
                
                Saludos,
                La Clínica.
                """
                if self.email_service.enviar_correo(turno.email_paciente, asunto, cuerpo):
                    enviados += 1
                else:
                    errores += 1
            else:
                print(f"El paciente {turno.paciente_nombre} no tiene email registrado.")
        
        return enviados, errores
