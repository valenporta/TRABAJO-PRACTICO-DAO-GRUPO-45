from datetime import datetime

from model.turno import Turno
from services.turno_service import TurnoService
from services.paciente_service import PacienteService
from services.medico_service import MedicoService


class TurnoController:

    def __init__(self):
        self.turno_service = TurnoService()
        self.paciente_service = PacienteService()
        self.medico_service = MedicoService()

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
            fecha_valida = datetime.strptime(fecha, "%Y-%m-%d").strftime("%Y-%m-%d")
        except ValueError:
            raise ValueError("La fecha debe tener formato YYYY-MM-DD.")

        hora = datos.get("hora")
        if not hora:
            raise ValueError("La hora es obligatoria.")

        try:
            hora_valida = datetime.strptime(hora, "%H:%M").strftime("%H:%M")
        except ValueError:
            raise ValueError("La hora debe tener formato HH:MM.")

        if self.turno_service.existe_conflicto(id_medico, fecha_valida, hora_valida, excluir_id=id_turno):
            raise ValueError("El medico ya tiene un turno asignado en ese horario.")

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