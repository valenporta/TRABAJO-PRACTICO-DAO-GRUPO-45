import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controller.reporte_controller import ReporteController

class ReportePacientesView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reporte de Pacientes Atendidos")
        self.geometry("900x650")
        self.controller = ReporteController()
        
        self._init_ui()

    def _init_ui(self):
        frame_filtros = tk.LabelFrame(self, text="Rango de Fechas")
        frame_filtros.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filtros, text="Desde (YYYY-MM-DD):").pack(side="left", padx=5)
        self.entry_desde = tk.Entry(frame_filtros)
        self.entry_desde.pack(side="left", padx=5)

        tk.Label(frame_filtros, text="Hasta (YYYY-MM-DD):").pack(side="left", padx=5)
        self.entry_hasta = tk.Entry(frame_filtros)
        self.entry_hasta.pack(side="left", padx=5)

        tk.Button(frame_filtros, text="Buscar", command=self._generar_reporte, bg="#4CAF50", fg="white").pack(side="left", padx=15)

        columnas = ("fecha", "hora", "nombre", "apellido", "dni", "medico", "estado")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings")
        
        self.tree.heading("fecha", text="Fecha")
        self.tree.heading("hora", text="Hora")
        self.tree.heading("nombre", text="Nombre")
        self.tree.heading("apellido", text="Apellido")
        self.tree.heading("dni", text="DNI")
        self.tree.heading("medico", text="Atendido por")
        self.tree.heading("estado", text="Estado")
        
        for col in columnas:
            self.tree.column(col, width=110)
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Footer ---
        frame_btns = tk.Frame(self)
        frame_btns.pack(pady=10)

        btn_csv = tk.Button(frame_btns, text="Exportar a CSV", command=self._exportar_csv, bg="#2196F3", fg="white", width=15)
        btn_csv.pack(side="left", padx=10)

        btn_pdf = tk.Button(frame_btns, text="Exportar a PDF", command=self._exportar_pdf, bg="#E91E63", fg="white", width=15)
        btn_pdf.pack(side="left", padx=10)

    def _generar_reporte(self):
        f_desde = self.entry_desde.get()
        f_hasta = self.entry_hasta.get()

        try:
            for item in self.tree.get_children():
                self.tree.delete(item)

            resultados = self.controller.obtener_reporte_pacientes(f_desde, f_hasta)
            
            if not resultados:
                messagebox.showinfo("Info", "No se encontraron pacientes atendidos en ese rango.")
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
            columnas = ["Fecha", "Hora", "Nombre", "Apellido", "DNI", "Médico", "Estado"]
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
            columnas = ["Fecha", "Hora", "Nombre", "Apellido", "DNI", "Médico", "Estado"]
            titulo = f"Reporte de Pacientes Atendidos ({self.entry_desde.get()} al {self.entry_hasta.get()})"
            try:
                self.controller.exportar_a_pdf(datos, columnas, filename, titulo)
                messagebox.showinfo("Éxito", "Reporte PDF generado correctamente.")
            except Exception as e:
                messagebox.showerror("Error", str(e))