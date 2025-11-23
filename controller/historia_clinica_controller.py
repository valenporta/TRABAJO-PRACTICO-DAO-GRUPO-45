from datetime import datetime

from services.paciente_service import PacienteService
from services.turno_service import TurnoService
from services.atencion_service import AtencionService
from services.historia_clinica_service import HistoriaClinicaService
from model.atencion import Atencion
from model.historia_clinica import HistoriaClinica


class HistoriaClinicaController:

    def __init__(self):
        self.paciente_service = PacienteService()
        self.turno_service = TurnoService()
        self.atencion_service = AtencionService()
        self.historia_service = HistoriaClinicaService()

    def listar_pacientes(self):
        return self.paciente_service.obtener_todos()

    def listar_turnos_paciente(self, id_paciente):
        paciente_id = self._parsear_id(id_paciente, "paciente")
        if not self.paciente_service.obtener_por_id(paciente_id):
            raise ValueError("El paciente indicado no existe.")
        return self.turno_service.obtener_por_paciente(paciente_id)

    def obtener_historia_paciente(self, id_paciente):
        paciente_id = self._parsear_id(id_paciente, "paciente")
        if not self.paciente_service.obtener_por_id(paciente_id):
            raise ValueError("El paciente indicado no existe.")
        return self.historia_service.listar_por_paciente(paciente_id)

    def obtener_atencion_por_turno(self, id_turno):
        turno_id = self._parsear_id(id_turno, "turno")
        return self.atencion_service.obtener_por_turno(turno_id)

    def registrar_atencion(self, datos: dict):
        id_paciente = self._parsear_id(datos.get("id_paciente"), "paciente")
        id_turno = self._parsear_id(datos.get("id_turno"), "turno")

        turno = self.turno_service.obtener_por_id(id_turno)
        if not turno:
            raise ValueError("El turno no existe.")
        if turno.id_paciente != id_paciente:
            raise ValueError("El turno no pertenece al paciente indicado.")

        diagnostico = (datos.get("diagnostico") or "").strip()
        if not diagnostico:
            raise ValueError("El diagnostico es obligatorio.")

        procedimiento = (datos.get("procedimiento") or "").strip() or None
        indicaciones = (datos.get("indicaciones") or "").strip() or None
        resumen = (datos.get("resumen") or "").strip()
        if not resumen:
            resumen = diagnostico

        fecha = (datos.get("fecha") or "").strip()
        if fecha:
            try:
                fecha_valida = datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-%m-%d")
            except ValueError as exc:
                raise ValueError("La fecha debe tener formato YYYY-MM-DD.") from exc
        else:
            fecha_valida = datetime.now().strftime("%Y-%m-%d")

        atencion_actual = self.atencion_service.obtener_por_turno(id_turno)
        if atencion_actual:
            atencion_actual.diagnostico = diagnostico
            atencion_actual.procedimiento = procedimiento
            atencion_actual.indicaciones = indicaciones
            self.atencion_service.actualizar(atencion_actual)
            atencion = atencion_actual
        else:
            atencion_nueva = Atencion(
                id_turno=id_turno,
                diagnostico=diagnostico,
                procedimiento=procedimiento,
                indicaciones=indicaciones,
            )
            atencion = self.atencion_service.crear(atencion_nueva)

        historia_actual = self.historia_service.obtener_por_atencion(atencion.id_atencion)
        if historia_actual:
            historia_actual.fecha = fecha_valida
            historia_actual.resumen = resumen
            historia_actual.id_atencion = atencion.id_atencion
            self.historia_service.actualizar(historia_actual)
            historia = historia_actual
        else:
            nueva_historia = HistoriaClinica(
                id_paciente=id_paciente,
                fecha=fecha_valida,
                resumen=resumen,
                id_atencion=atencion.id_atencion,
            )
            historia = self.historia_service.crear(nueva_historia)

        estado_atendido = self._obtener_estado_turno("Atendido")
        if estado_atendido and turno.id_estado != estado_atendido.id_estado:
            turno.id_estado = estado_atendido.id_estado
            turno.estado_nombre = estado_atendido.nombre
            self.turno_service.actualizar(turno)

        return historia

    def _parsear_id(self, valor, nombre):
        if valor is None or valor == "":
            raise ValueError(f"El ID de {nombre} es obligatorio.")
        try:
            numero = int(valor)
        except (TypeError, ValueError) as exc:
            raise ValueError(f"El ID de {nombre} debe ser numerico.") from exc
        if numero <= 0:
            raise ValueError(f"El ID de {nombre} debe ser positivo.")
        return numero

    def _obtener_estado_turno(self, nombre_estado):
        for estado in self.turno_service.obtener_estados():
            if estado.nombre.lower() == nombre_estado.lower():
                return estado
        return None
