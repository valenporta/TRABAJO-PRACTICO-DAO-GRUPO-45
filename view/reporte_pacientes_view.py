import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controller.reporte_controller import ReporteController

class ReportePacientesView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reporte de Pacientes Atendidos")
        self.geometry("900x600")
        self.controller = ReporteController()
        
        self._init_ui()

    def _init_ui(self):
        # --- Filtros ---
        frame_filtros = tk.LabelFrame(self, text="Rango de Fechas")
        frame_filtros.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filtros, text="Desde (YYYY-MM-DD):").pack(side="left", padx=5)
        self.entry_desde = tk.Entry(frame_filtros)
        self.entry_desde.pack(side="left", padx=5)

        tk.Label(frame_filtros, text="Hasta (YYYY-MM-DD):").pack(side="left", padx=5)
        self.entry_hasta = tk.Entry(frame_filtros)
        self.entry_hasta.pack(side="left", padx=5)

        tk.Button(frame_filtros, text="Buscar", command=self._generar_reporte, bg="#4CAF50", fg="white").pack(side="left", padx=15)

        # --- Tabla ---
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
        btn_export = tk.Button(self, text="Exportar a CSV", command=self._exportar, bg="#2196F3", fg="white")
        btn_export.pack(pady=10)

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

    def _exportar(self):
        items = self.tree.get_children()
        if not items:
            messagebox.showwarning("Atención", "No hay datos para exportar.")
            return

        filename = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])
        if not filename:
            return

        datos = []
        for item in items:
            datos.append(self.tree.item(item)['values'])

        columnas = ["Fecha", "Hora", "Nombre", "Apellido", "DNI", "Médico", "Estado"]
        try:
            self.controller.exportar_a_csv(datos, columnas, filename)
            messagebox.showinfo("Éxito", "Reporte exportado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))