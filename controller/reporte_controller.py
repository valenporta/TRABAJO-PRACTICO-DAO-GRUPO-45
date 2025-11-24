import csv
from datetime import datetime

from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle
from reportlab.lib.styles import getSampleStyleSheet

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

    # --------------------------------------------------------------------------
    # EXPORTACIÓN A CSV
    # --------------------------------------------------------------------------
    def exportar_a_csv(self, datos, columnas, ruta_archivo):
        if not datos:
            raise ValueError("No hay datos para exportar.")
        try:
            with open(ruta_archivo, mode='w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(columnas)
                writer.writerows(datos)
        except Exception as e:
            raise Exception(f"Error al exportar archivo CSV: {str(e)}")

    # --------------------------------------------------------------------------
    # NUEVO: EXPORTACIÓN A PDF CON REPORTLAB
    # --------------------------------------------------------------------------
    def exportar_a_pdf(self, datos, columnas, ruta_archivo, titulo_reporte):
        """
        Genera un PDF con una tabla formateada según el manual de ReportLab.
        """
        if not datos:
            raise ValueError("No hay datos para exportar.")

        try:

            doc = SimpleDocTemplate(ruta_archivo, pagesize=letter)
            elements = []

            styles = getSampleStyleSheet()

            elements.append(Paragraph(titulo_reporte, styles['Title']))
            elements.append(Spacer(1, 12)) 

            data_tabla = [columnas] + [list(fila) for fila in datos]

            t = Table(data_tabla)

            style = TableStyle([
                ('BACKGROUND', (0, 0), (-1, 0), colors.grey),     
                ('TEXTCOLOR', (0, 0), (-1, 0), colors.whitesmoke),  
                ('ALIGN', (0, 0), (-1, -1), 'CENTER'),              
                ('FONTNAME', (0, 0), (-1, 0), 'Helvetica-Bold'),   
                ('BOTTOMPADDING', (0, 0), (-1, 0), 12),            
                ('BACKGROUND', (0, 1), (-1, -1), colors.beige),     
                ('GRID', (0, 0), (-1, -1), 1, colors.black)    
            ])
            t.setStyle(style)

            elements.append(t)

            doc.build(elements)

        except Exception as e:
            raise Exception(f"Error al generar el PDF: {str(e)}")

    def _validar_fechas(self, f_inicio, f_fin):
        if not f_inicio or not f_fin:
            raise ValueError("Las fechas de inicio y fin son obligatorias.")
        try:
            d_inicio = datetime.strptime(f_inicio, "%Y-%m-%d")
            d_fin = datetime.strptime(f_fin, "%Y-%m-%d")
        except ValueError:
            raise ValueError("El formato de fecha debe ser YYYY-MM-DD.")
        if d_inicio > d_fin:
            raise ValueError("La fecha de inicio no puede ser mayor a la fecha de fin.")