# view/paciente_view.py

# view/paciente_view.py

import tkinter as tk
from tkinter import ttk, messagebox
# Asegúrate de que PacienteController esté disponible y tenga la lógica actualizada
from controller.paciente_controller import PacienteController 


class PacienteView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.controller = PacienteController()
        # Inicializamos selected_id para rastrear qué paciente estamos editando/eliminando
        self.selected_id = None 
        self.pack(fill="both", expand=True)

        self.create_widgets()
        self.cargar_pacientes()

    # -------------------------------------------
    # Crear UI
    # -------------------------------------------
    def create_widgets(self):
        # ----- FORMULARIO -----
        form_frame = tk.LabelFrame(self, text="Datos del Paciente")
        form_frame.pack(fill="x", padx=10, pady=10)

        # DNI
        tk.Label(form_frame, text="DNI:").grid(row=0, column=0, sticky="e", padx=5, pady=5)
        self.entry_dni = tk.Entry(form_frame)
        self.entry_dni.grid(row=0, column=1, padx=5, pady=5)

        # Nombre
        tk.Label(form_frame, text="Nombre:").grid(row=1, column=0, sticky="e", padx=5, pady=5)
        self.entry_nombre = tk.Entry(form_frame)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        # Apellido
        tk.Label(form_frame, text="Apellido:").grid(row=2, column=0, sticky="e", padx=5, pady=5)
        self.entry_apellido = tk.Entry(form_frame)
        self.entry_apellido.grid(row=2, column=1, padx=5, pady=5)

        # Teléfono
        tk.Label(form_frame, text="Teléfono:").grid(row=3, column=0, sticky="e", padx=5, pady=5)
        self.entry_telefono = tk.Entry(form_frame)
        self.entry_telefono.grid(row=3, column=1, padx=5, pady=5)

        # Email
        tk.Label(form_frame, text="Email:").grid(row=4, column=0, sticky="e", padx=5, pady=5)
        self.entry_email = tk.Entry(form_frame)
        self.entry_email.grid(row=4, column=1, padx=5, pady=5)

        # Fecha de nacimiento
        tk.Label(form_frame, text="Fecha Nac (YYYY-MM-DD):").grid(row=5, column=0, sticky="e", padx=5, pady=5)
        self.entry_fecha = tk.Entry(form_frame)
        self.entry_fecha.grid(row=5, column=1, padx=5, pady=5)

        # BOTONES
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Guardar", command=self.guardar_paciente, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Actualizar", command=self.actualizar_paciente, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Eliminar", command=self.eliminar_paciente, width=12).pack(side="left", padx=5)
        tk.Button(btn_frame, text="Limpiar", command=self.limpiar_formulario, width=12).pack(side="left", padx=5)

        # ----- TABLA -----
        tabla_frame = tk.Frame(self)
        tabla_frame.pack(fill="both", expand=True, padx=10, pady=10)

        columnas = ("id", "dni", "nombre", "apellido", "telefono", "email", "fecha_nac")

        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=10)

        for col in columnas:
            self.tabla.heading(col, text=col.capitalize())
            self.tabla.column(col, width=120)

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    # -------------------------------------------
    # Cargar pacientes en tabla
    # -------------------------------------------
    def cargar_pacientes(self):
        # Limpiar tabla
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        # Cargar datos
        pacientes = self.controller.listar_pacientes()
        for p in pacientes:
            self.tabla.insert("", "end", values=(
                p.id_paciente,
                p.dni,
                p.nombre,
                p.apellido,
                p.telefono,
                p.email,
                p.fecha_nac
            ))

    # -------------------------------------------
    # Guardar nuevo paciente
    # -------------------------------------------
    def guardar_paciente(self):
        try:
            datos = {
                "dni": self.entry_dni.get(),
                "nombre": self.entry_nombre.get(),
                "apellido": self.entry_apellido.get(),
                "telefono": self.entry_telefono.get(),
                "email": self.entry_email.get(),
                "fecha_nac": self.entry_fecha.get()
            }

            self.controller.crear_paciente(datos)
            messagebox.showinfo("Éxito", "Paciente creado correctamente.")
            self.cargar_pacientes()
            self.limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------------------------------------------
    # Seleccionar fila de tabla
    # -------------------------------------------
    def seleccionar_fila(self, event):
        seleccionado = self.tabla.focus()
        if not seleccionado:
            return

        datos = self.tabla.item(seleccionado, "values")

        # Guardar el ID seleccionado para las operaciones de Actualizar/Eliminar
        self.selected_id = datos[0] 

        # Completar formulario
        self.entry_dni.delete(0, tk.END)
        self.entry_dni.insert(0, datos[1])

        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, datos[2])

        self.entry_apellido.delete(0, tk.END)
        self.entry_apellido.insert(0, datos[3])

        self.entry_telefono.delete(0, tk.END)
        self.entry_telefono.insert(0, datos[4])

        self.entry_email.delete(0, tk.END)
        self.entry_email.insert(0, datos[5])

        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, datos[6])

    # -------------------------------------------
    # Actualizar paciente (Función del botón)
    # -------------------------------------------
    def actualizar_paciente(self):
        try:
            # 1. Verificar si hay un ID seleccionado
            if self.selected_id is None:
                raise ValueError("Seleccione un paciente de la tabla.")

            # 2. Recolectar datos del formulario
            datos = {
                "dni": self.entry_dni.get(),
                "nombre": self.entry_nombre.get(),
                "apellido": self.entry_apellido.get(),
                "telefono": self.entry_telefono.get(),
                "email": self.entry_email.get(),
                "fecha_nac": self.entry_fecha.get()
            }
            
            # 3. Llamar al controlador. El controlador se encarga de la validación
            #    del DNI excluyendo self.selected_id.
            self.controller.actualizar_paciente(self.selected_id, datos) 
            
            messagebox.showinfo("Éxito", "Paciente actualizado correctamente.")
            self.cargar_pacientes()
            self.limpiar_formulario() # Limpiar después de la operación

        except Exception as e:
            # Captura el error lanzado por el controlador (incluyendo "Ya existe otro paciente con ese DNI.")
            messagebox.showerror("Error", str(e))

    # -------------------------------------------
    # Eliminar paciente
    # -------------------------------------------
    def eliminar_paciente(self):
        try:
            if self.selected_id is None:
                raise ValueError("Seleccione un paciente para eliminar.")

            if messagebox.askyesno("Confirmar", "¿Eliminar este paciente?"):
                self.controller.eliminar_paciente(self.selected_id)
                messagebox.showinfo("Éxito", "Paciente eliminado.")
                self.cargar_pacientes()
                self.limpiar_formulario()

        except Exception as e:
            messagebox.showerror("Error", str(e))

    # -------------------------------------------
    # Limpiar formulario
    # -------------------------------------------
    def limpiar_formulario(self):
        self.entry_dni.delete(0, tk.END)
        self.entry_nombre.delete(0, tk.END)
        self.entry_apellido.delete(0, tk.END)
        self.entry_telefono.delete(0, tk.END)
        self.entry_email.delete(0, tk.END)
        self.entry_fecha.delete(0, tk.END)

        # ⚠️ IMPORTANTE: Resetear el ID seleccionado después de limpiar
        self.selected_id = None