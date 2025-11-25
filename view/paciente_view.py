import tkinter as tk
from tkinter import ttk, messagebox
from controller.paciente_controller import PacienteController
# Asegúrate de que RecordatorioController esté disponible
from controller.recordatorio_controller import RecordatorioController


class PacienteView(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.controller = PacienteController()
        self.selected_id = None 
        self.pack(fill="both", expand=True)

        self.create_widgets()
        self.cargar_pacientes()

    # -------------------------------------------
    # Crear UI 
    # -------------------------------------------
    def create_widgets(self):
        # Usamos ttk.LabelFrame para el estilo 'clam'
        form = ttk.LabelFrame(self, text="👤 Datos del Paciente")
        form.pack(fill="x", padx=15, pady=15)
        
        # Frame interno para controlar el grid
        form_grid = tk.Frame(form)
        form_grid.pack(padx=10, pady=5)

        # DNI
        tk.Label(form_grid, text="DNI:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_dni = ttk.Entry(form_grid, width=30) # Usamos ttk.Entry
        self.entry_dni.grid(row=0, column=1, padx=5, pady=5)

        # Nombre
        tk.Label(form_grid, text="Nombre:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_nombre = ttk.Entry(form_grid, width=30)
        self.entry_nombre.grid(row=1, column=1, padx=5, pady=5)

        # Apellido
        tk.Label(form_grid, text="Apellido:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_apellido = ttk.Entry(form_grid, width=30)
        self.entry_apellido.grid(row=2, column=1, padx=5, pady=5)
        
        # Teléfono
        tk.Label(form_grid, text="Teléfono:").grid(row=0, column=2, sticky="w", padx=20, pady=5)
        self.entry_telefono = ttk.Entry(form_grid, width=30)
        self.entry_telefono.grid(row=0, column=3, padx=5, pady=5)

        # Email
        tk.Label(form_grid, text="Email:").grid(row=1, column=2, sticky="w", padx=20, pady=5)
        self.entry_email = ttk.Entry(form_grid, width=30)
        self.entry_email.grid(row=1, column=3, padx=5, pady=5)

        # Fecha de nacimiento
        tk.Label(form_grid, text="Fecha Nac (YYYY-MM-DD):").grid(row=2, column=2, sticky="w", padx=20, pady=5)
        self.entry_fecha = ttk.Entry(form_grid, width=30)
        self.entry_fecha.grid(row=2, column=3, padx=5, pady=5)


        # --- BOTONES (CENTRADOS) ---
        
        # Contenedor principal que ocupa todo el ancho
        btns = tk.Frame(self)
        btns.pack(fill="x", padx=15, pady=10)
        
        # Contenedor interno para centrar los botones
        center_frame = tk.Frame(btns)
        center_frame.pack(anchor="center") 

        # Los botones se empaquetan en el center_frame, usando style='TButton'
        ttk.Button(center_frame, text="Guardar", command=self.guardar_paciente, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Actualizar", command=self.actualizar_paciente, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Eliminar", command=self.eliminar_paciente, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Limpiar", command=self.limpiar_formulario, style='TButton').pack(side="left", padx=5)
        
        # Botón Recordatorios (Usando estilo específico, si el 'TButton' no es deseado, lo mantenemos separado)
        # Lo mantendremos con un estilo separado para que destaque (color amarillo)
        ttk.Button(center_frame, text="Recordatorios", command=self.enviar_recordatorios, 
                   # Creamos un estilo específico para este botón
                   style='Yellow.TButton').pack(side="left", padx=15)
        
        # Configurar el estilo amarillo para que el botón destaque
        style = ttk.Style()
        style.configure('Yellow.TButton', background='#FFC107', foreground='black')
        style.map('Yellow.TButton', background=[('active', '#e6b200')])

        # ----- TABLA -----
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columnas = ("id", "dni", "nombre", "apellido", "telefono", "email", "fecha_nac")
        self.tabla = ttk.Treeview(table_frame, columns=columnas, show="headings", height=10)

        # Configuración de encabezados y ordenamiento
        for col in columnas:
            self.tabla.heading(col, text=col.replace('_', ' ').capitalize(), command=lambda c=col: self.ordenar_columna(c, False))
            self.tabla.column(col, width=110)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar_fila)

    # -------------------------------------------
    # Ordenar columnas (Mantenido)
    # -------------------------------------------
    def ordenar_columna(self, col, reverse):
        # Obtener datos de la tabla
        l = [(self.tabla.set(k, col), k) for k in self.tabla.get_children('')]
        
        # Intentar convertir a numero si es posible (para ID y DNI)
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(key=lambda t: t[0].lower(), reverse=reverse)

        # Reordenar items
        for index, (val, k) in enumerate(l):
            self.tabla.move(k, '', index)

        # Actualizar comando para invertir orden en el proximo click
        self.tabla.heading(col, command=lambda: self.ordenar_columna(col, not reverse))


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

        # Limpiar y Completar formulario
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
            
            # 3. Llamar al controlador para actualización (incluye validación DNI)
            self.controller.actualizar_paciente(self.selected_id, datos) 
            
            messagebox.showinfo("Éxito", "Paciente actualizado correctamente.")
            self.cargar_pacientes()
            self.limpiar_formulario() 

        except Exception as e:
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

        self.selected_id = None

    # -------------------------------------------
    # Enviar Recordatorios
    # -------------------------------------------
    def enviar_recordatorios(self):
        if messagebox.askyesno("Confirmar", "¿Desea enviar los recordatorios para los turnos de mañana?"):
            try:
                controller = RecordatorioController()
                enviados, errores = controller.enviar_recordatorios_manana()
                messagebox.showinfo("Proceso Finalizado", f"Se enviaron {enviados} recordatorios.\nErrores/Sin email: {errores}")
            except Exception as e:
                messagebox.showerror("Error", f"Ocurrió un error: {str(e)}")