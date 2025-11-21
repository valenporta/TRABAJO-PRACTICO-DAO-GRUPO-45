import tkinter as tk
from services.database import DatabaseConnection
from view.paciente_view import PacienteView

if __name__ == "__main__":
    # Inicializar base de datos
    db = DatabaseConnection()
    db.initialize_database()

    root = tk.Tk()
    root.title("Sistema de Turnos - Pacientes")
    root.geometry("800x600")

    PacienteView(root)

    root.mainloop()
