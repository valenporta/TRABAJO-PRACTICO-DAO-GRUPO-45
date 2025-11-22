import tkinter as tk
from tkinter import ttk

# Inicialización de Base de Datos
from services.database import DatabaseConnection

# Vistas
from view.paciente_view import PacienteView
from view.medico_view import MedicoView
from view.especialidad_view import EspecialidadView


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


# -----------------------------------------
# PROGRAMA PRINCIPAL
# -----------------------------------------
if __name__ == "__main__":
    # Crear DB si no existe
    db = DatabaseConnection()
    db.initialize_database()

    root = tk.Tk()
    root.title("Sistema de Turnos Médicos")
    root.geometry("400x400")

    MenuPrincipal(root)

    root.mainloop()
