from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

from services.paciente_service import PacienteService
from services.turno_service import TurnoService
from services.atencion_service import AtencionService
from services.historia_clinica_service import HistoriaClinicaService
from services.receta_service import RecetaService
from services.medico_service import MedicoService
from model.atencion import Atencion
from model.historia_clinica import HistoriaClinica
from model.receta import Receta


class HistoriaClinicaController:

    def __init__(self):
        self.paciente_service = PacienteService()
        self.turno_service = TurnoService()
        self.atencion_service = AtencionService()
        self.historia_service = HistoriaClinicaService()
        self.receta_service = RecetaService()
        self.medico_service = MedicoService()

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

        # --- RECETA ELECTRONICA ---
        detalle_receta = (datos.get("receta_detalle") or "").strip()
        receta_creada = None
        if detalle_receta:
            # Verificar si ya existe receta para esta atencion (opcional, aqui asumimos una por atencion)
            receta_existente = self.receta_service.obtener_por_atencion(atencion.id_atencion)
            if not receta_existente:
                nueva_receta = Receta(
                    id_atencion=atencion.id_atencion,
                    fecha=fecha_valida,
                    detalle=detalle_receta
                )
                receta_creada = self.receta_service.crear(nueva_receta)
            else:
                # Si ya existe, podriamos actualizarla o dejarla como esta.
                # Por simplicidad, retornamos la existente para generar PDF si se pide.
                receta_creada = receta_existente

        estado_atendido = self._obtener_estado_turno("Atendido")
        if estado_atendido and turno.id_estado != estado_atendido.id_estado:
            turno.id_estado = estado_atendido.id_estado
            turno.estado_nombre = estado_atendido.nombre
            self.turno_service.actualizar(turno)

        return historia, receta_creada

    def crear_receta(self, id_atencion, detalle, fecha, diagnostico):
        if not detalle:
            raise ValueError("El detalle de la receta no puede estar vacío.")
        
        receta_existente = self.receta_service.obtener_por_atencion(id_atencion)
        if receta_existente:
            # Si existe, actualizamos el detalle (opcional) o retornamos la existente
            # Vamos a actualizarla para permitir correcciones
            # Pero RecetaService no tiene actualizar... vamos a asumir que creamos una nueva si no existe
            # Ojo: RecetaService.crear hace INSERT.
            # Deberíamos implementar actualizar en RecetaService si queremos editar.
            # Por ahora, retornamos la existente y avisamos? O simplemente retornamos.
            return receta_existente
        
        nueva_receta = Receta(
            id_atencion=id_atencion,
            fecha=fecha,    
            detalle=detalle,
            diagnostico=diagnostico
        )
        return self.receta_service.crear(nueva_receta)

    def generar_pdf_receta(self, id_receta, ruta_archivo):
        # Obtener datos completos para el PDF
        # Necesitamos: Receta, Atencion, Turno, Medico, Paciente
        # Como no tenemos un metodo que traiga todo junto, lo buscamos por partes.
        
        # 1. Receta (aunque ya tenemos el ID, podriamos pasar el objeto, pero mejor buscarlo para asegurar)
        # Como RecetaService.obtener_por_id no existe en el plan, usamos obtener_por_atencion si tenemos id_atencion
        # Pero aqui solo llega id_receta. Asumiremos que el caller tiene la receta o modificamos el service.
        # Para simplificar, asumiremos que el caller paso el objeto receta o que modificamos el service.
        # Vamos a asumir que el caller pasa el objeto receta o que buscamos por atencion si tenemos el dato.
        # REVISION: El metodo recibe id_receta. Pero RecetaService no tiene obtener_por_id.
        # Vamos a agregar obtener_por_id al service o cambiar este metodo para recibir el objeto Receta.
        # Mejor cambiamos este metodo para recibir el objeto Receta completo y los datos necesarios.
        pass 

    def generar_pdf_receta_data(self, receta, paciente, medico, ruta_archivo, diagnostico):
        try:
            doc = SimpleDocTemplate(ruta_archivo, pagesize=letter)
            elements = []
            styles = getSampleStyleSheet()

            # Encabezado
            elements.append(Paragraph("RECETA MÉDICA ELECTRÓNICA", styles['Title']))
            elements.append(Spacer(1, 12))

            # Datos del Medico
            datos_medico = [
                [f"Dr/a: {medico.apellido}, {medico.nombre}"],
                [f"Matrícula: {medico.matricula}"],
                [f"Fecha: {receta.fecha}"]
            ]
            t_medico = Table(datos_medico, colWidths=[400])
            t_medico.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT'), ('FONTNAME', (0,0), (-1,-1), 'Helvetica-Bold')]))
            elements.append(t_medico)
            elements.append(Spacer(1, 12))

            # Datos del Paciente
            datos_paciente = [
                [f"Paciente: {paciente.apellido}, {paciente.nombre}"],
                [f"DNI: {paciente.dni}"],
                [f"Diagnostico: {diagnostico}"],
            ]
            t_paciente = Table(datos_paciente, colWidths=[400])
            t_paciente.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'LEFT')]))
            elements.append(t_paciente)
            elements.append(Spacer(1, 20))

            # Detalle de la Receta
            elements.append(Paragraph("Prescripción:", styles['Heading3']))
            elements.append(Spacer(1, 5))
            elements.append(Paragraph(receta.detalle, styles['BodyText']))
            elements.append(Spacer(1, 40))

            # Firma (Simulada)
            elements.append(Paragraph("_" * 30, styles['Normal']))
            elements.append(Paragraph("Firma y Sello del Médico", styles['Normal']))

            doc.build(elements)
        except Exception as e:
            raise Exception(f"Error al generar PDF de receta: {str(e)}")

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
