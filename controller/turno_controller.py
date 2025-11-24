from datetime import datetime, timedelta

from model.turno import Turno
from services.turno_service import TurnoService
from services.paciente_service import PacienteService
from services.medico_service import MedicoService
from services.agenda_service import AgendaService


class TurnoController:

    def __init__(self):
        self.turno_service = TurnoService()
        self.paciente_service = PacienteService()
        self.medico_service = MedicoService()
        # Inicializamos el servicio de agenda
        self.agenda_service = AgendaService()

    def registrar_turno(self, datos: dict):
        turno = self._construir_turno(None, datos)
        return self.turno_service.crear(turno)

    def actualizar_turno(self, id_turno, datos: dict):
        actual = self.turno_service.obtener_por_id(id_turno)
        if not actual:
            raise ValueError("El turno no existe.")

        turno = self._construir_turno(id_turno, datos)
        return self.turno_service.actualizar(turno)

    def eliminar_turno(self, id_turno):
        if not self.turno_service.obtener_por_id(id_turno):
            raise ValueError("El turno no existe.")
        self.turno_service.eliminar(id_turno)

    def listar_turnos(self):
        return self.turno_service.obtener_todos()

    def listar_estados(self):
        return self.turno_service.obtener_estados()

    def listar_pacientes(self):
        return self.paciente_service.obtener_todos()

    def listar_medicos(self):
        return self.medico_service.obtener_todos()

    def _construir_turno(self, id_turno, datos: dict):
        id_paciente = self._parsear_id(datos.get("id_paciente"), "paciente")
        id_medico = self._parsear_id(datos.get("id_medico"), "medico")
        id_estado = self._parsear_id(datos.get("id_estado"), "estado")

        if not any(estado.id_estado == id_estado for estado in self.turno_service.obtener_estados()):
            raise ValueError("El estado seleccionado no existe.")

        if not self.paciente_service.obtener_por_id(id_paciente):
            raise ValueError("No existe un paciente con ese ID.")

        if not self.medico_service.obtener_por_id(id_medico):
            raise ValueError("No existe un medico con ese ID.")

        fecha = datos.get("fecha")
        if not fecha:
            raise ValueError("La fecha es obligatoria.")

        try:
            fecha_dt = datetime.strptime(fecha, "%Y-%m-%d")
            fecha_valida = fecha_dt.strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener formato YYYY-MM-DD.")

        hora = datos.get("hora")
        if not hora:
            raise ValueError("La hora es obligatoria.")

        try:
            hora_dt = datetime.strptime(hora, "%H:%M")
            hora_valida = hora_dt.strftime("%H:%M")
        except ValueError:
            raise ValueError("La hora debe tener formato HH:MM.")

        # --- VALIDACIONES DE AGENDA ---

        # 1. Verificar si el medico trabaja ese dia
        dia_semana = fecha_dt.weekday()
        agenda = self.agenda_service.obtener_por_medico_y_dia(id_medico, dia_semana)

        if not agenda:
            dias_nombres = ["Lunes", "Martes", "Miercoles", "Jueves", "Viernes", "Sabado", "Domingo"]
            raise ValueError(f"El medico no tiene agenda configurada para los dias {dias_nombres[dia_semana]}.")

        duracion_min = agenda.duracion_turno_min
        
        nuevo_inicio = hora_dt
        nuevo_fin = nuevo_inicio + timedelta(minutes=duracion_min)

        agenda_inicio = datetime.strptime(agenda.hora_desde, "%H:%M")
        agenda_fin = datetime.strptime(agenda.hora_hasta, "%H:%M")

        if nuevo_inicio < agenda_inicio or nuevo_fin > agenda_fin:
             raise ValueError(f"El turno debe ser entre {agenda.hora_desde} y {agenda.hora_hasta} (Duracion: {duracion_min} min).")

        turnos_existentes = self.turno_service.obtener_turnos_medico_fecha(id_medico, fecha_valida)

        for t in turnos_existentes:
            if id_turno and int(t["id_turno"]) == int(id_turno):
                continue
            t_inicio = datetime.strptime(t["hora"], "%H:%M")
            t_fin = t_inicio + timedelta(minutes=duracion_min)

            if nuevo_inicio < t_fin and nuevo_fin > t_inicio:
                 raise ValueError(f"El horario se superpone con otro turno existente a las {t['hora']}.")

        # --- FIN VALIDACIONES ---

        motivo = datos.get("motivo") or None

        return Turno(
            id_paciente=id_paciente,
            id_medico=id_medico,
            fecha=fecha_valida,
            hora=hora_valida,
            id_estado=id_estado,
            motivo=motivo,
            id_turno=id_turno,
        )

    @staticmethod
    def _parsear_id(valor, nombre_campo):
        if valor is None or valor == "":
            raise ValueError(f"El ID de {nombre_campo} es obligatorio.")

        try:
            numero = int(valor)
        except (TypeError, ValueError):
            raise ValueError(f"El ID de {nombre_campo} debe ser numerico.")

        if numero <= 0:
            raise ValueError(f"El ID de {nombre_campo} debe ser positivo.")

        return numero