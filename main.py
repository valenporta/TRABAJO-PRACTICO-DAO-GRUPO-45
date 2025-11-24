import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk 
import os

# Inicialización de Base de Datos
from services.database import DatabaseConnection
from services.data_seeder import DataSeeder

# Vistas existentes
from view.paciente_view import PacienteView
from view.medico_view import MedicoView
from view.especialidad_view import EspecialidadView
from view.agenda_view import AgendaView
from view.turno_view import TurnoView
from view.historia_clinica_view import HistoriaClinicaView

from view.reporte_medico_view import ReporteMedicoView
from view.reporte_pacientes_view import ReportePacientesView


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
        
        self.menu_frame = tk.Frame(self, bg="#F0F0F0")
        self.menu_frame.pack(fill="x", pady=10, padx=20)

        # Separador visual
        ttk.Separator(self.menu_frame, orient='horizontal').pack(fill='x', padx=20, pady=10)

        # --- Botones del menú ---
        ttk.Button(self.menu_frame, text="ABM Pacientes",
                  command=self.abrir_pacientes, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="ABM Médicos",
                  command=self.abrir_medicos, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="ABM Especialidades",
                  command=self.abrir_especialidades, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="Gestión de Agenda",
                  command=self.abrir_agenda, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="Registro de Turnos",
              command=self.abrir_turnos, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="Historia Clinica",
                command=self.abrir_historia, width=25).pack(fill="x", pady=5)

        ttk.Button(self.menu_frame, text="Reportes",
                command=self.abrir_menu_reportes, width=25).pack(fill="x", pady=5)


    # -----------------------------------------
    # Logica del Menú de Reportes
    # -----------------------------------------
    def abrir_menu_reportes(self):
        ventana_rep = tk.Toplevel(self)
        ventana_rep.title("Seleccionar Reporte")
        ventana_rep.geometry("300x200")
        ventana_rep.resizable(False, False)
        
        x = self.master.winfo_x() + (self.master.winfo_width() // 2) - 150
        y = self.master.winfo_y() + (self.master.winfo_height() // 2) - 100
        ventana_rep.geometry(f"+{x}+{y}")

        lbl = tk.Label(ventana_rep, text="Seleccione el reporte a generar:", font=("Arial", 10))
        lbl.pack(pady=15)

        ttk.Button(ventana_rep, text="Turnos por Médico", 
                   command=lambda: [self.abrir_reporte_medico(), ventana_rep.destroy()], 
                   width=25).pack(pady=5)

        ttk.Button(ventana_rep, text="Pacientes Atendidos", 
                   command=lambda: [self.abrir_reporte_pacientes(), ventana_rep.destroy()], 
                   width=25).pack(pady=5)


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

    def abrir_historia(self):
        ventana = tk.Toplevel(self)
        ventana.title("Historia Clinica")
        ventana.geometry("1000x700")
        HistoriaClinicaView(ventana)
    
    # -----------------------------------------
    # Abrir ventanas de Reportes (Vistas que son Toplevel)
    # -----------------------------------------
    def abrir_reporte_medico(self):
        # CORRECCIÓN: Instanciamos directamente porque la clase hereda de Toplevel
        ReporteMedicoView(self)

    def abrir_reporte_pacientes(self):
        # CORRECCIÓN: Instanciamos directamente porque la clase hereda de Toplevel
        ReportePacientesView(self)

    def cargar_header(self, path, width):
        """Carga y muestra la imagen de encabezado."""
        try:
            img = Image.open(path)
            ratio = width / img.width
            height = int(img.height * ratio)
            img = img.resize((width, height), Image.LANCZOS)
            
            self.header_img = ImageTk.PhotoImage(img)
            tk.Label(self.header_frame, image=self.header_img, bg="#FFFFFF").pack(anchor="center", padx=10, pady=5)
            
        except FileNotFoundError:
            tk.Label(self.header_frame, text="Sistema de Turnos Médicos",
                     font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=20)
        except Exception as e:
            tk.Label(self.header_frame, text="Sistema de Turnos Médicos",
                     font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=20)


# -----------------------------------------
# PROGRAMA PRINCIPAL
# -----------------------------------------

if __name__ == "__main__":
    # Crear DB si no existe
    db = DatabaseConnection()
    db.initialize_database()

    seeder = DataSeeder()
    seeder.run()

    root = tk.Tk()

    root.geometry("400x750")
    root.title("Sistema de Turnos Médicos")
    root.resizable(False, False)

    MenuPrincipal(root)

    root.mainloop()