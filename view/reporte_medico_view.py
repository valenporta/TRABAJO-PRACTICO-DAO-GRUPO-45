import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controller.reporte_controller import ReporteController

class ReporteMedicoView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reporte de Turnos por Médico")
        self.geometry("900x650")
        self.controller = ReporteController()
        self.medicos_map = {} 

        self._init_ui()

    def _init_ui(self):
        # --- Filtros ---
        frame_filtros = tk.LabelFrame(self, text="Filtros de Búsqueda")
        frame_filtros.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filtros, text="Médico:").grid(row=0, column=0, padx=5, pady=5)
        self.combo_medicos = ttk.Combobox(frame_filtros, state="readonly", width=30)
        self.combo_medicos.grid(row=0, column=1, padx=5, pady=5)
        self._cargar_medicos()

        tk.Label(frame_filtros, text="Desde (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
        self.entry_desde = tk.Entry(frame_filtros)
        self.entry_desde.grid(row=0, column=3, padx=5, pady=5)

        tk.Label(frame_filtros, text="Hasta (YYYY-MM-DD):").grid(row=0, column=4, padx=5, pady=5)
        self.entry_hasta = tk.Entry(frame_filtros)
        self.entry_hasta.grid(row=0, column=5, padx=5, pady=5)

        tk.Button(frame_filtros, text="Generar", command=self._generar_reporte, bg="#4CAF50", fg="white").grid(row=0, column=6, padx=10, pady=5)

        # --- Tabla ---
        columnas = ("fecha", "hora", "paciente", "dni", "estado", "motivo")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings")
        
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("paciente", text="Paciente")
        self.tree.heading("dni", text="DNI Paciente")
        self.tree.heading("estado", text="Estado Turno")
        self.tree.heading("motivo", text="Motivo")
        
        for col in columnas:
            self.tree.column(col, width=120)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Footer (Botones de Exportación) ---
        frame_btns = tk.Frame(self)
        frame_btns.pack(pady=10)

        btn_csv = tk.Button(frame_btns, text="Exportar a CSV", command=self._exportar_csv, bg="#2196F3", fg="white", width=15)
        btn_csv.pack(side="left", padx=10)

        btn_pdf = tk.Button(frame_btns, text="Exportar a PDF", command=self._exportar_pdf, bg="#E91E63", fg="white", width=15)
        btn_pdf.pack(side="left", padx=10)

    def _cargar_medicos(self):
        medicos = self.controller.listar_medicos()
        values = []
        for m in medicos:
            display = f"{m.apellido}, {m.nombre} (Mat: {m.matricula})"
            self.medicos_map[display] = m.id_medico
            values.append(display)
        self.combo_medicos['values'] = values

    def _generar_reporte(self):
        medico_display = self.combo_medicos.get()
        f_desde = self.entry_desde.get()
        f_hasta = self.entry_hasta.get()

        if not medico_display:
            messagebox.showwarning("Atención", "Seleccione un médico.")
            return

        id_medico = self.medicos_map.get(medico_display)

        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            resultados = self.controller.obtener_reporte_turnos_medico(id_medico, f_desde, f_hasta)
            
            if not resultados:
                messagebox.showinfo("Info", "No se encontraron turnos en ese rango.")
                return

            for row in resultados:
                self.tree.insert("", "end", values=row)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _obtener_datos_actuales(self):
        items = self.tree.get_children()
        if not items:
            return None
        datos = []
        for item in items:
            datos.append(self.tree.item(item)['values'])
        return datos

    def _exportar_csv(self):
        datos = self._obtener_datos_actuales()
        if not datos:
            messagebox.showwarning("Atención", "No hay datos para exportar.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if filename:
            columnas = ["Fecha", "Hora", "Paciente", "DNI", "Estado", "Motivo"]
            try:
                self.controller.exportar_a_csv(datos, columnas, filename)
                messagebox.showinfo("Éxito", "Reporte CSV exportado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", str(e))

    def _exportar_pdf(self):
        datos = self._obtener_datos_actuales()
        if not datos:
            messagebox.showwarning("Atención", "No hay datos para exportar.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF Files", "*.pdf")])
        if filename:
            columnas = ["Fecha", "Hora", "Paciente", "DNI", "Estado", "Motivo"]
            titulo = f"Reporte de Turnos - Médico: {self.combo_medicos.get()}"
            try:
                self.controller.exportar_a_pdf(datos, columnas, filename, titulo)
                messagebox.showinfo("Éxito", "Reporte PDF generado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", str(e))