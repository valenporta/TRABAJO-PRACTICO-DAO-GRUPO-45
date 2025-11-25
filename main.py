import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk 
import os

# Inicialización de Base de Datos
from services.database import DatabaseConnection

# Vistas existentes
from view.paciente_view import PacienteView
from view.medico_view import MedicoView
from view.especialidad_view import EspecialidadView
from view.agenda_view import AgendaView
from view.turno_view import TurnoView
from view.historia_clinica_view import HistoriaClinicaView
from view.registrar_atencion_view import RegistrarAtencionView

from view.reporte_medico_view import ReporteMedicoView
from view.reporte_pacientes_view import ReportePacientesView
from view.reporte_especialidad_view import ReporteEspecialidadView
from view.reporte_estadistico_view import ReporteEstadisticoView

from tkinter import messagebox


class MenuPrincipal(tk.Frame):
    def __init__(self, master):
        style = ttk.Style()
        style.theme_use('clam')
        style.configure('TButton', font=('Arial', 10, 'bold'), 
                        padding=10, 
                        background='#4CAF50', 
                        foreground='white')
        style.map('TButton', background=[('active', '#45a049')])
        
        super().__init__(master, bg="#F0F0F0") # Fondo gris claro
        self.pack(fill="both", expand=True)
        
        self.header_frame = tk.Frame(self, bg="#FFFFFF")
        self.header_frame.pack(fill="x", pady=(0, 10))
        self.cargar_header("img/Sist.png", width=320)
        
        # --- IMPLEMENTACIÓN DEL SCROLLBAR PARA EL MENÚ ---
        self.canvas = tk.Canvas(self, bg="#F0F0F0", highlightthickness=0)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.menu_frame = tk.Frame(self.canvas, bg="#F0F0F0")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        
        # Asegura que el scrollregion se ajuste al tamaño del frame contenido
        self.menu_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion = self.canvas.bbox("all")
            )
        )
        
        # Centrar el frame del menú en el canvas
        self.canvas.create_window((200, 0), window=self.menu_frame, anchor="n") # 200 es aprox la mitad de 400 (ancho ventana)
        
        # Ajustar ancho del canvas al redimensionar
        self.bind("<Configure>", self._on_resize)

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Bind mouse wheel for scrolling
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)

        # Separador visual
        ttk.Separator(self.menu_frame, orient='horizontal').pack(fill='x', padx=20, pady=10)

        # --- Botones del menú ---
        ttk.Button(self.menu_frame, text="Gestion de Pacientes",
                  command=self.abrir_pacientes, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="Gestion de Médicos",
                  command=self.abrir_medicos, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="Gestion de Especialidades",
                  command=self.abrir_especialidades, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="Gestión de Agenda",
                  command=self.abrir_agenda, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="Registro de Turnos",
              command=self.abrir_turnos, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="Registrar Atención",
                command=self.abrir_registrar_atencion, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="Historia Clinica",
                command=self.abrir_historia, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="Reportes",
                command=self.abrir_menu_reportes, width=25).pack(fill="x", pady=5)


    def _on_mousewheel(self, event):
        self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")

    def _on_resize(self, event):
        # Actualizar la posición del window en el canvas para mantenerlo centrado
        width = event.width
        # Solo actualizamos si el canvas tiene items
        if self.canvas.find_all():
             self.canvas.coords(self.canvas.find_all()[0], width // 2, 0)

    # -----------------------------------------
    # Logica del Menú de Reportes
    # -----------------------------------------
    def abrir_menu_reportes(self):
        ventana_rep = tk.Toplevel(self)
        ventana_rep.title("Seleccionar Reporte")
        ventana_rep.geometry("300x250") # Aumenté un poco el alto
        ventana_rep.resizable(False, False)
        
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - 150
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - 125
        ventana_rep.geometry(f"+{x}+{y}")

        lbl = tk.Label(ventana_rep, text="Seleccione el reporte a generar:", font=("Arial", 10))
        lbl.pack(pady=10)

        ttk.Button(ventana_rep, text="Turnos por Médico", 
                   command=lambda: [self.abrir_reporte_medico(), ventana_rep.destroy()], 
                   width=25).pack(pady=3)

        ttk.Button(ventana_rep, text="Pacientes Atendidos", 
                   command=lambda: [self.abrir_reporte_pacientes(), ventana_rep.destroy()], 
                   width=25).pack(pady=3)

        ttk.Button(ventana_rep, text="Turnos por Especialidad", 
                   command=lambda: [self.abrir_reporte_especialidad(), ventana_rep.destroy()], 
                   width=25).pack(pady=3)

        ttk.Button(ventana_rep, text="Estadística de Asistencia", 
                   command=lambda: [self.abrir_reporte_estadistico(), ventana_rep.destroy()], 
                   width=25).pack(pady=3)


    # -----------------------------------------
    # Abrir ventanas
    # -----------------------------------------

    def abrir_pacientes(self):
        ventana = tk.Toplevel(self)
        ventana.title("ABM Pacientes")
        ventana.geometry("850x600")
        PacienteView(ventana)

    def abrir_medicos(self):
        ventana = tk.Toplevel(self)
        ventana.title("ABM Médicos")
        ventana.geometry("850x600")
        MedicoView(ventana)

    def abrir_especialidades(self):
        ventana = tk.Toplevel(self)
        ventana.title("ABM Especialidades")
        ventana.geometry("500x400")
        EspecialidadView(ventana)

    def abrir_agenda(self):
        ventana = tk.Toplevel(self)
        ventana.title("Gestión de Agenda Médica")
        ventana.geometry("900x600")
        AgendaView(ventana)

    def abrir_turnos(self):
        ventana = tk.Toplevel(self)
        ventana.title("Registro de Turnos")
        ventana.geometry("900x600")
        TurnoView(ventana)

    def abrir_registrar_atencion(self):
        ventana = tk.Toplevel(self)
        ventana.title("Registrar Atención")
        ventana.geometry("1000x700")
        RegistrarAtencionView(ventana)

    def abrir_historia(self):
        ventana = tk.Toplevel(self)
        ventana.title("Historia Clinica")
        ventana.geometry("1000x700")
        HistoriaClinicaView(ventana)
    
    # -----------------------------------------
    # Abrir ventanas de Reportes (Vistas que son Toplevel)
    # -----------------------------------------
    def abrir_reporte_medico(self):
        ReporteMedicoView(self)

    def abrir_reporte_pacientes(self):
        ReportePacientesView(self)

    def abrir_reporte_especialidad(self):
        ReporteEspecialidadView(self)

    def abrir_reporte_estadistico(self):
        ReporteEstadisticoView(self)

    def cargar_header(self, path, width):
        
        base_dir = os.path.dirname(os.path.abspath(__file__))
        
        ruta_completa = os.path.join(base_dir, path)
        
        try:
            img = Image.open(ruta_completa) 
            
            ratio = width / img.width
            height = int(img.height * ratio)
            img = img.resize((width, height), Image.LANCZOS)
            
            self.header_img = ImageTk.PhotoImage(img)
            tk.Label(self.header_frame, image=self.header_img, bg="#FFFFFF").pack(anchor="center", padx=10, pady=5)
            
        except FileNotFoundError:
            # Informa la ruta que falló para depuración
            print(f"Error: No se encontró el archivo de imagen en la ruta: {ruta_completa}") 
            tk.Label(self.header_frame, text="Sistema de Turnos Médicos",
                     font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=20)
        except Exception as e:
            print(f"Error al cargar la imagen: {e}")
            tk.Label(self.header_frame, text="Sistema de Turnos Médicos",
                     font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=20)


# -----------------------------------------
# PROGRAMA PRINCIPAL
# -----------------------------------------

if __name__ == "__main__":
    # Crear DB si no existe
    db = DatabaseConnection()
    db.initialize_database()

    root = tk.Tk()

    root.geometry("400x600")
    root.title("Sistema de Turnos Médicos")
    root.resizable(False, False)

    MenuPrincipal(root)

    root.mainloop()