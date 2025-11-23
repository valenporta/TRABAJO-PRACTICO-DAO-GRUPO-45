import tkinter as tk
from tkinter import ttk

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
        super().__init__(master)
        self.pack(fill="both", expand=True)

        tk.Label(self, text="Sistema de Turnos Médicos",
                 font=("Arial", 18, "bold")).pack(pady=20)

        # Botones del menú
        tk.Button(self, text="ABM Pacientes",
                  command=self.abrir_pacientes, width=25).pack(pady=10)

        tk.Button(self, text="ABM Médicos",
                  command=self.abrir_medicos, width=25).pack(pady=10)

        tk.Button(self, text="ABM Especialidades",
                  command=self.abrir_especialidades, width=25).pack(pady=10)

        tk.Button(self, text="Gestión de Agenda",
                  command=self.abrir_agenda, width=25).pack(pady=10)

        tk.Button(self, text="Registro de Turnos",
              command=self.abrir_turnos, width=25).pack(pady=10)

        tk.Button(self, text="Historia Clinica",
                command=self.abrir_historia, width=25).pack(pady=10)

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
# PROGRAMA PRINCIPAL
# -----------------------------------------

if __name__ == "__main__":
    # Crear DB si no existe
    db = DatabaseConnection()
    db.initialize_database()

    seeder = DataSeeder()
    seeder.run()

    root = tk.Tk()
    root.title("Sistema de Turnos Médicos")
    # Ajusté la altura a 500 para que quepa el nuevo botón
    root.geometry("400x640") 

    MenuPrincipal(root)

    root.mainloop()