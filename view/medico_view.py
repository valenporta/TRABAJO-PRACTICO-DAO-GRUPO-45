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
        self.selected_id = None 
        self.create_widgets()
        self.cargar_medicos()
        self.cargar_especialidades()


    def create_widgets(self):
        # Usamos ttk.LabelFrame para el estilo 'clam'
        form = ttk.LabelFrame(self, text="👨‍⚕️ Datos del Médico")
        form.pack(fill="x", padx=15, pady=15)
        
        # Frame interno para controlar el grid y el padding
        form_grid = tk.Frame(form)
        form_grid.pack(padx=10, pady=5)
        
        # DNI
        tk.Label(form_grid, text="DNI:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.dni = ttk.Entry(form_grid, width=30) 
        self.dni.grid(row=0, column=1, padx=5, pady=5)
        
        # Matrícula
        tk.Label(form_grid, text="Matrícula:").grid(row=0, column=2, sticky="w", padx=20, pady=5)
        self.matricula = ttk.Entry(form_grid, width=30)
        self.matricula.grid(row=0, column=3, padx=5, pady=5)

        # Nombre
        tk.Label(form_grid, text="Nombre:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.nombre = ttk.Entry(form_grid, width=30)
        self.nombre.grid(row=1, column=1, padx=5, pady=5)

        # Teléfono
        tk.Label(form_grid, text="Teléfono:").grid(row=1, column=2, sticky="w", padx=20, pady=5)
        self.telefono = ttk.Entry(form_grid, width=30)
        self.telefono.grid(row=1, column=3, padx=5, pady=5)

        # Apellido
        tk.Label(form_grid, text="Apellido:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.apellido = ttk.Entry(form_grid, width=30)
        self.apellido.grid(row=2, column=1, padx=5, pady=5)

        # Especialidad
        tk.Label(form_grid, text="Especialidad:").grid(row=2, column=2, sticky="w", padx=20, pady=5)
        self.cb_especialidad = ttk.Combobox(form_grid, state="readonly", width=28)
        self.cb_especialidad.grid(row=2, column=3, padx=5, pady=5)


        
        # Contenedor principal que ocupa todo el ancho
        btns = tk.Frame(self)
        btns.pack(fill="x", padx=15, pady=10)
        
        # Contenedor interno para centrar los botones
        center_frame = tk.Frame(btns)
        center_frame.pack(anchor="center") 

        # Los botones se empaquetan en el center_frame
        ttk.Button(center_frame, text="Guardar", command=self.guardar, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Actualizar", command=self.actualizar, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Eliminar", command=self.eliminar, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Limpiar", command=self.limpiar, style='TButton').pack(side="left", padx=5)

        # TABLA
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        cols = ("id", "dni", "nombre", "apellido", "matricula", "telefono", "especialidades")
        self.tabla = ttk.Treeview(table_frame, columns=cols, show="headings")

        # Configuración de Encabezados y Anchos
        self.tabla.heading("id", text="ID", anchor="center")
        self.tabla.heading("dni", text="DNI")
        self.tabla.heading("nombre", text="Nombre")
        self.tabla.heading("apellido", text="Apellido")
        self.tabla.heading("matricula", text="Matrícula")
        self.tabla.heading("telefono", text="Teléfono")
        self.tabla.heading("especialidades", text="Especialidad(es)")

        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("dni", width=100)
        self.tabla.column("nombre", width=120)
        self.tabla.column("apellido", width=120)
        self.tabla.column("matricula", width=80)
        self.tabla.column("telefono", width=100)
        self.tabla.column("especialidades", width=150)
        
        # Añadir Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
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
            # Obtener el nombre de la especialidad
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
        
        # Llenar el Combobox con el formato "ID - Nombre"
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
            if not self.selected_id:
                 raise ValueError("Seleccione un médico de la tabla para actualizar.")
                 
            # 1. Obtener la especialidad seleccionada del Combobox
            especialidad_seleccionada = self.cb_especialidad.get()
            
            if " - " not in especialidad_seleccionada:
                raise ValueError("Debe seleccionar una especialidad válida de la lista.")

            id_especialidad_nuevo = int(especialidad_seleccionada.split(" - ")[0])

            # 2. Recolectar datos incluyendo el ID de la especialidad
            datos = {
                "dni": self.dni.get(),
                "nombre": self.nombre.get(),
                "apellido": self.apellido.get(),
                "matricula": self.matricula.get(),
                "telefono": self.telefono.get(),
                "id_especialidad": id_especialidad_nuevo 
            }
            
            self.controller.actualizar_medico(self.selected_id, datos)
            messagebox.showinfo("Éxito", "Médico actualizado.")
            self.cargar_medicos() 
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
        
        
        especialidad_actual_nombre = vals[6] 
        
        found_value = ""
        for item_cb in self.cb_especialidad['values']:
            if especialidad_actual_nombre and especialidad_actual_nombre in item_cb:
                found_value = item_cb
                break
        
        self.cb_especialidad.set(found_value)

    def eliminar(self):
        try:
            if not self.selected_id:
                 raise ValueError("Seleccione un médico para eliminar.")
            if messagebox.askyesno("Confirmar", "¿Eliminar médico?"):
                self.controller.eliminar_medico(self.selected_id)
                messagebox.showinfo("Éxito", "Médico eliminado.")
                self.cargar_medicos()
                self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def limpiar(self):
        self.dni.delete(0, tk.END)
        self.nombre.delete(0, tk.END)
        self.apellido.delete(0, tk.END)
        self.matricula.delete(0, tk.END)
        self.telefono.delete(0, tk.END)
        self.cb_especialidad.set("") 
        self.selected_id = None