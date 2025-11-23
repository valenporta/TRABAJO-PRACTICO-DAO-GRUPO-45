import tkinter as tk
from tkinter import ttk
from PIL import Image, ImageTk 
import os

# Inicialización de Base de Datos
from services.database import DatabaseConnection
from services.data_seeder import DataSeeder
# Vistas
from view.paciente_view import PacienteView
from view.medico_view import MedicoView
from view.especialidad_view import EspecialidadView
from view.agenda_view import AgendaView
from view.turno_view import TurnoView
from view.historia_clinica_view import HistoriaClinicaView


class MenuPrincipal(tk.Frame):
    def __init__(self, master):
        style = ttk.Style()
        # Puedes probar 'clam', 'alt', 'default', 'classic'. 'clam' suele ser limpio.
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
        self.cargar_header("img/Sist.png", width=320) # Asume imagen de 380px de ancho
        
        self.menu_frame = tk.Frame(self, bg="#F0F0F0")
        self.menu_frame.pack(fill="x", pady=10, padx=20)

        # Separador visual
        ttk.Separator(self.menu_frame, orient='horizontal').pack(fill='x', padx=20, pady=10)

        # Botones del menú
        ttk.Button(self.menu_frame, text="ABM Pacientes",
                  command=self.abrir_pacientes, width=25).pack(fill="x", pady=10)

        ttk.Button(self.menu_frame, text="ABM Médicos",
                  command=self.abrir_medicos, width=25).pack(fill="x", pady=10)

        ttk.Button(self.menu_frame, text="ABM Especialidades",
                  command=self.abrir_especialidades, width=25).pack(fill="x", pady=10)

        ttk.Button(self.menu_frame, text="Gestión de Agenda",
                  command=self.abrir_agenda, width=25).pack(fill="x", pady=10)

        ttk.Button(self.menu_frame, text="Registro de Turnos",
              command=self.abrir_turnos, width=25).pack(fill="x", pady=10)

        ttk.Button(self.menu_frame, text="Historia Clinica",
                command=self.abrir_historia, width=25).pack(fill="x", pady=10)

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
    
    def cargar_header(self, path, width):
        """Carga y muestra la imagen de encabezado."""
        try:
            img = Image.open(path)
            # Redimensionar la imagen para que encaje
            ratio = width / img.width
            height = int(img.height * ratio)
            img = img.resize((width, height), Image.LANCZOS)
            
            # Almacenar la referencia para que Tkinter no la borre
            self.header_img = ImageTk.PhotoImage(img)
            tk.Label(self.header_frame, image=self.header_img, bg="#FFFFFF").pack(anchor="center", padx=10, pady=5)
            
        except FileNotFoundError:
            print(f"Advertencia: No se encontró la imagen del encabezado en {path}.")
            tk.Label(self.header_frame, text="Sistema de Turnos Médicos",
                     font=("Arial", 18, "bold"), bg="#FFFFFF").pack(pady=20)
        except Exception as e:
            print(f"Error al cargar la imagen del encabezado: {e}")
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
    # Ajusté la altura a 500 para que quepa el nuevo botón
    root.geometry("400x750")
    root.title("Sistema de Turnos Médicos")
    root.resizable(False, False)

    MenuPrincipal(root)

    root.mainloop()