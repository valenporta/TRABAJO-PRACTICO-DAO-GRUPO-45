
import tkinter as tk
from tkinter import ttk, messagebox
from controller.medico_controller import MedicoController
from services.especialidad_service import EspecialidadService
from services.medico_especialidad_service import MedicoEspecialidadService

class MedicoView(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.controller = MedicoController()
        self.pack(fill="both", expand=True)
        self.especialidad_service = EspecialidadService()
        self.medico_esp_service = MedicoEspecialidadService()
        self.create_widgets()
        self.cargar_medicos()
        self.cargar_especialidades()

    # ------------------------------
    # UI
    # ------------------------------
    def create_widgets(self):
        form = tk.LabelFrame(self, text="Datos del Médico")
        form.pack(fill="x", padx=10, pady=10)

        # DNI
        tk.Label(form, text="DNI:").grid(row=0, column=0, sticky="w")
        self.dni = tk.Entry(form)
        self.dni.grid(row=0, column=1)

        # Nombre
        tk.Label(form, text="Nombre:").grid(row=1, column=0, sticky="w")
        self.nombre = tk.Entry(form)
        self.nombre.grid(row=1, column=1)

        # Apellido
        tk.Label(form, text="Apellido:").grid(row=2, column=0, sticky="w")
        self.apellido = tk.Entry(form)
        self.apellido.grid(row=2, column=1)

        # Matrícula
        tk.Label(form, text="Matrícula:").grid(row=3, column=0, sticky="w")
        self.matricula = tk.Entry(form)
        self.matricula.grid(row=3, column=1)

        # Teléfono
        tk.Label(form, text="Teléfono:").grid(row=4, column=0, sticky="w")
        self.telefono = tk.Entry(form)
        self.telefono.grid(row=4, column=1)

        # Especialidad
        tk.Label(form, text="Especialidad:").grid(row=5, column=0, sticky="w")
        self.cb_especialidad = ttk.Combobox(form, state="readonly")
        self.cb_especialidad.grid(row=5, column=1, padx=5, pady=5)

        # BOTONES
        btns = tk.Frame(self)
        btns.pack(fill="x", padx=10, pady=10)

        tk.Button(btns, text="Guardar", command=self.guardar).pack(side="left", padx=5)
        tk.Button(btns, text="Actualizar", command=self.actualizar).pack(side="left", padx=5)
        tk.Button(btns, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        tk.Button(btns, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)

        # TABLA
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("id", "dni", "nombre", "apellido", "matricula", "telefono", "especialidades")
        self.tabla = ttk.Treeview(table_frame, columns=cols, show="headings")

        for c in cols:
            self.tabla.heading(c, text=c.capitalize())
            self.tabla.column(c, width=120)

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    # ------------------------------
    # CRUD
    # ------------------------------
    def cargar_medicos(self):
        for row in self.tabla.get_children():
            self.tabla.delete(row)

        medicos = self.controller.listar_medicos()

        for m in medicos:
            especialidades = self.medico_esp_service.obtener_especialidades_de_medico(m.id_medico)
            esp_str = ", ".join(especialidades) if especialidades else "—"

            self.tabla.insert("", "end", values=(
                m.id_medico,
                m.dni,
                m.nombre,
                m.apellido,
                m.matricula,
                m.telefono,
                esp_str
            ))

    def cargar_especialidades(self):
        especialidades = self.especialidad_service.obtener_todas()
        print("DEBUG:", especialidades)

        self.cb_especialidad["values"] = [
            f"{e.id_especialidad} - {e.nombre}" for e in especialidades
        ]

    def guardar(self):
        try:
            datos = {
                "dni": self.dni.get(),
                "nombre": self.nombre.get(),
                "apellido": self.apellido.get(),
                "matricula": self.matricula.get(),
                "telefono": self.telefono.get(),
                "id_especialidad": int(self.cb_especialidad.get().split(" - ")[0])
            }
            self.controller.crear_medico(datos)
            messagebox.showinfo("Éxito", "Médico agregado.")
            self.cargar_medicos()
            self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        try:
            # 1. Obtener la especialidad seleccionada del Combobox
            especialidad_seleccionada = self.cb_especialidad.get()
            
            # 2. Extraer el ID de la especialidad (ej: "4 - Ginecología" -> 4)
            # Asumo que el Combobox está poblado con strings del tipo "ID - Nombre"
            if " - " not in especialidad_seleccionada:
                 raise ValueError("Debe seleccionar una especialidad válida de la lista.")

            id_especialidad_nuevo = int(especialidad_seleccionada.split(" - ")[0])

            # 3. Recolectar datos incluyendo el ID de la especialidad
            datos = {
                "dni": self.dni.get(),
                "nombre": self.nombre.get(),
                "apellido": self.apellido.get(),
                "matricula": self.matricula.get(),
                "telefono": self.telefono.get(),
                "id_especialidad": id_especialidad_nuevo # <-- ¡SOLUCIÓN!
            }
            
            self.controller.actualizar_medico(self.selected_id, datos)
            messagebox.showinfo("Éxito", "Médico actualizado.")
            self.cargar_medicos() # Recargar la tabla para mostrar el cambio
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------------------
    # Auxiliares: Seleccionar fila (Cambio 2)
    # ------------------------------
    def seleccionar(self, event):
        item = self.tabla.focus()
        vals = self.tabla.item(item, "values")
        if not vals:
            return

        self.selected_id = vals[0]

        self.dni.delete(0, tk.END)
        self.dni.insert(0, vals[1])

        self.nombre.delete(0, tk.END)
        self.nombre.insert(0, vals[2])

        self.apellido.delete(0, tk.END)
        self.apellido.insert(0, vals[3])

        self.matricula.delete(0, tk.END)
        self.matricula.insert(0, vals[4])

        self.telefono.delete(0, tk.END)
        self.telefono.insert(0, vals[5])
        
        # -------------------------------------------------------------
        # SOLUCIÓN DE VISUALIZACIÓN: Cargar Especialidad seleccionada
        # -------------------------------------------------------------
        especialidad_actual_nombre = vals[6] # Asumo que el nombre de la especialidad está en la columna 6 de la tabla
        
        # Recorre las opciones del Combobox (ej: ["1 - Pediatría", "2 - Cardiología"])
        found_value = ""
        for item_cb in self.cb_especialidad['values']:
            # Busca la opción que contenga el nombre de la especialidad actual
            if especialidad_actual_nombre and especialidad_actual_nombre in item_cb:
                found_value = item_cb
                break
        
        self.cb_especialidad.set(found_value)

    def eliminar(self):
        try:
            if messagebox.askyesno("Confirmar", "¿Eliminar médico?"):
                self.controller.eliminar_medico(self.selected_id)
                messagebox.showinfo("Éxito", "Médico eliminado.")
                self.cargar_medicos()
                self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ------------------------------
    # Auxiliares
    # ------------------------------
    def seleccionar(self, event):
        item = self.tabla.focus()
        vals = self.tabla.item(item, "values")
        if not vals:
            return

        self.selected_id = vals[0]

        self.dni.delete(0, tk.END)
        self.dni.insert(0, vals[1])

        self.nombre.delete(0, tk.END)
        self.nombre.insert(0, vals[2])

        self.apellido.delete(0, tk.END)
        self.apellido.insert(0, vals[3])

        self.matricula.delete(0, tk.END)
        self.matricula.insert(0, vals[4])

        self.telefono.delete(0, tk.END)
        self.telefono.insert(0, vals[5])

    def limpiar(self):
        self.dni.delete(0, tk.END)
        self.nombre.delete(0, tk.END)
        self.apellido.delete(0, tk.END)
        self.matricula.delete(0, tk.END)
        self.telefono.delete(0, tk.END)
        self.selected_id = None
