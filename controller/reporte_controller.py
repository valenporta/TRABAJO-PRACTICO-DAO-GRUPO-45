import csv
from datetime import datetime

from services.medico_service import MedicoService
from services.turno_service import TurnoService
from services.paciente_service import PacienteService

class ReporteController:
    def __init__(self):
        self.medico_service = MedicoService()
        self.turno_service = TurnoService()
        self.paciente_service = PacienteService()

    def listar_medicos(self):
        return self.medico_service.obtener_todos()

    def obtener_reporte_turnos_medico(self, id_medico, f_inicio, f_fin):
        self._validar_fechas(f_inicio, f_fin)
        if not id_medico:
            raise ValueError("Debe seleccionar un médico.")
        
        return self.turno_service.obtener_turnos_por_medico_y_rango(id_medico, f_inicio, f_fin)
import csv
from datetime import datetime

from services.medico_service import MedicoService
from services.turno_service import TurnoService
from services.paciente_service import PacienteService

class ReporteController:
    def __init__(self):
        self.medico_service = MedicoService()
        self.turno_service = TurnoService()
        self.paciente_service = PacienteService()

    def listar_medicos(self):
        return self.medico_service.obtener_todos()

    def obtener_reporte_turnos_medico(self, id_medico, f_inicio, f_fin):
        self._validar_fechas(f_inicio, f_fin)
        if not id_medico:
            raise ValueError("Debe seleccionar un médico.")
        
        return self.turno_service.obtener_turnos_por_medico_y_rango(id_medico, f_inicio, f_fin)

    def obtener_reporte_pacientes(self, f_inicio, f_fin):
        self._validar_fechas(f_inicio, f_fin)

        return self.paciente_service.obtener_pacientes_atendidos_en_rango(f_inicio, f_fin)

    def obtener_reporte_especialidad(self, f_inicio=None, f_fin=None):
        if f_inicio or f_fin:
            self._validar_fechas(f_inicio, f_fin)
        return self.turno_service.obtener_cantidad_turnos_por_especialidad(f_inicio, f_fin)

    def obtener_reporte_estados(self, f_inicio=None, f_fin=None):
        if f_inicio or f_fin:
            self._validar_fechas(f_inicio, f_fin)
        return self.turno_service.obtener_cantidad_turnos_por_estado(f_inicio, f_fin)

    def exportar_a_csv(self, datos, columnas, ruta_archivo):
        if not datos:
            raise ValueError("No hay datos para exportar.")
        
        try:
            with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(columnas)  # Escribir encabezados
                writer.writerows(datos)    # Escribir datos
        except Exception as e:
            raise Exception(f"Error al exportar archivo: {str(e)}")

    def _validar_fechas(self, f_inicio, f_fin):
        if not f_inicio or not f_fin:
            raise ValueError("Las fechas de inicio y fin son obligatorias si se filtra por fecha.")
        
        try:
            d_inicio = datetime.strptime(f_inicio, "%Y-%m-%d")
            d_fin = datetime.strptime(f_fin, "%Y-%m-%d")
        except ValueError:
            raise ValueError("El formato de fecha debe ser YYYY-MM-DD.")

        if d_inicio > d_fin:
            raise ValueError("La fecha de inicio no puede ser mayor a la fecha de fin.")