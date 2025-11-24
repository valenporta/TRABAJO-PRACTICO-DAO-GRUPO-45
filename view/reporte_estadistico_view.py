import tkinter as tk
from tkinter import ttk, messagebox
from controller.reporte_controller import ReporteController
import math

class ReporteEstadisticoView(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Estadística de Asistencia")
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

        tk.Button(frame_filtros, text="Generar Gráfico", command=self._generar_grafico, bg="#4CAF50", fg="white").grid(row=0, column=4, padx=10, pady=5)

        # --- Canvas para el gráfico ---
        self.canvas_frame = tk.Frame(self, bg="white")
        self.canvas_frame.pack(fill="both", expand=True, padx=10, pady=10)
        
        self.canvas = tk.Canvas(self.canvas_frame, bg="white")
        self.canvas.pack(fill="both", expand=True)
        self.canvas.bind("<Configure>", self._on_resize)

        self.datos_actuales = None

        # Forzar actualización de geometría antes de dibujar
        self.update_idletasks()
        
        # Generar gráfico inicial (sin filtros)
        self._generar_grafico()

    def _generar_grafico(self):
        f_desde = self.entry_desde.get()
        f_hasta = self.entry_hasta.get()

        # Si los campos están vacíos, pasamos None
        if not f_desde: f_desde = None
        if not f_hasta: f_hasta = None

        try:
            resultados = self.controller.obtener_reporte_estados(f_desde, f_hasta)
            self.datos_actuales = resultados
            
            if not resultados:
                messagebox.showinfo("Info", "No se encontraron datos.")
                self.canvas.delete("all")
                return

            self._dibujar_grafico_torta(resultados)

        except ValueError as e:
            messagebox.showerror("Error", str(e))

    def _on_resize(self, event):
        if self.datos_actuales:
            self._dibujar_grafico_torta(self.datos_actuales)

    def _dibujar_grafico_torta(self, datos):
        self.canvas.delete("all")
        
        # datos es una lista de tuplas (estado, cantidad)
        total = sum(d[1] for d in datos)
        if total == 0:
            return

        width = self.canvas.winfo_width()
        height = self.canvas.winfo_height()
        
        # Si las dimensiones son muy pequeñas (ej. al inicio), no dibujar aún
        if width < 50 or height < 50:
            return

        x_center = width // 2 - 100 # Desplazar un poco a la izquierda para leyenda
        y_center = height // 2
        radius = min(width, height) // 3

        start_angle = 0
        colors = ["#4CAF50", "#F44336", "#FFC107", "#2196F3", "#9C27B0", "#FF5722"]
        
        # Leyenda
        legend_x = x_center + radius + 50
        legend_y = y_center - radius

        for i, (estado, cantidad) in enumerate(datos):
            extent = (cantidad / total) * 360
            color = colors[i % len(colors)]
            
            # Ajuste para evitar problemas con arcos de 360 grados en algunas plataformas
            if extent >= 360:
                self.canvas.create_oval(
                    x_center - radius, y_center - radius,
                    x_center + radius, y_center + radius,
                    fill=color, outline="white"
                )
            else:
                self.canvas.create_arc(
                    x_center - radius, y_center - radius,
                    x_center + radius, y_center + radius,
                    start=start_angle, extent=extent,
                    fill=color, outline="white"
                )
            
            # Dibujar leyenda
            self.canvas.create_rectangle(
                legend_x, legend_y + (i * 30),
                legend_x + 20, legend_y + (i * 30) + 20,
                fill=color, outline="black"
            )
            
            porcentaje = (cantidad / total) * 100
            texto_leyenda = f"{estado}: {cantidad} ({porcentaje:.1f}%)"
            self.canvas.create_text(
                legend_x + 30, legend_y + (i * 30) + 10,
                text=texto_leyenda, anchor="w", font=("Arial", 10)
            )

            start_angle += extent
