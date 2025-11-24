import tkinter as tk
from tkinter import ttk, messagebox, filedialog
from controller.reporte_controller import ReporteController

class ReporteEspecialidadView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Reporte de Turnos por Especialidad")
        self.geometry("800x600")
        self.controller = ReporteController()

        self._init_ui()

    def _init_ui(self):
        # --- Filtros ---
        frame_filtros = tk.LabelFrame(self, text="Filtros de Búsqueda")
        frame_filtros.pack(fill="x", padx=10, pady=5)

        tk.Label(frame_filtros, text="Desde (YYYY-MM-DD):").grid(row=0, column=0, padx=5, pady=5)
        self.entry_desde = tk.Entry(frame_filtros)
        self.entry_desde.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(frame_filtros, text="Hasta (YYYY-MM-DD):").grid(row=0, column=2, padx=5, pady=5)
        self.entry_hasta = tk.Entry(frame_filtros)
        self.entry_hasta.grid(row=0, column=3, padx=5, pady=5)

        tk.Button(frame_filtros, text="Generar Reporte", command=self._generar_reporte, bg="#4CAF50", fg="white").grid(row=0, column=4, padx=10, pady=5)

        # --- Tabla ---
        columnas = ("especialidad", "cantidad")
        self.tree = ttk.Treeview(self, columns=columnas, show="headings")
        
        self.tree.heading("especialidad", text="Especialidad")
        self.tree.heading("cantidad", text="Cantidad de Turnos")
        
        self.tree.column("especialidad", width=300)
        self.tree.column("cantidad", width=150, anchor="center")
        
        self.tree.pack(fill="both", expand=True, padx=10, pady=10)

        # --- Footer ---
        btn_export = tk.Button(self, text="Exportar a CSV", command=self._exportar, bg="#2196F3", fg="white")
        btn_export.pack(pady=10)

        # Cargar reporte inicial (sin filtros)
        self._generar_reporte()

    def _generar_reporte(self):
        f_desde = self.entry_desde.get()
        f_hasta = self.entry_hasta.get()
        
        # Si los campos están vacíos, pasamos None
        if not f_desde: f_desde = None
        if not f_hasta: f_hasta = None

        try:
            # Limpiar tabla
            for item in self.tree.get_children():
                self.tree.delete(item)

            resultados = self.controller.obtener_reporte_especialidad(f_desde, f_hasta)
            
            if not resultados:
                messagebox.showinfo("Info", "No se encontraron turnos.")
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

        columnas = ["Especialidad", "Cantidad"]
        try:
            self.controller.exportar_a_csv(datos, columnas, filename)
            messagebox.showinfo("Éxito", "Reporte exportado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", str(e))
