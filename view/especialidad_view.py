# view/especialidad_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from controller.especialidad_controller import EspecialidadController

class EspecialidadView(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.controller = EspecialidadController()
        self.selected_id = None
        self.pack(fill="both", expand=True)

        self.create_widgets()
        self.cargar()

    def create_widgets(self):
        
        form = ttk.LabelFrame(self, text="🏷️ Gestión de Especialidades")
        form.pack(fill="x", padx=15, pady=15) 
        
        # Contenedor interno para centrar los campos
        form_grid = tk.Frame(form)
        form_grid.pack(padx=10, pady=5, anchor="center") # Centrar los campos

        tk.Label(form_grid, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nombre = ttk.Entry(form_grid, width=30) # Usamos ttk.Entry
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        # --- BOTONES (CENTRADOS) ---
        
        # Contenedor principal que ocupa todo el ancho
        btns = tk.Frame(self)
        btns.pack(fill="x", padx=15, pady=10)
        
        # Contenedor interno para centrar los botones
        center_frame = tk.Frame(btns)
        center_frame.pack(anchor="center") 

        # Los botones se empaquetan en el center_frame, usando style='TButton'
        ttk.Button(center_frame, text="Guardar", command=self.guardar, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Actualizar", command=self.actualizar, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Eliminar", command=self.eliminar, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Limpiar", command=self.limpiar, style='TButton').pack(side="left", padx=5)

        # Tabla 
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10) # Mayor padding

        cols = ("id", "nombre")
        self.tabla = ttk.Treeview(table_frame, columns=cols, show="headings")

        self.tabla.heading("id", text="ID", anchor="center")
        self.tabla.heading("nombre", text="Nombre")

        self.tabla.column("id", width=60, anchor="center")
        self.tabla.column("nombre", width=250)
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    # -----------------------------
    # Funciones CRUD
    # -----------------------------
    
    def cargar(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        especialidades = self.controller.listar_especialidades()
        for e in especialidades:
            self.tabla.insert("", "end", values=(e.id_especialidad, e.nombre))

    def guardar(self):
        try:
            datos = {"nombre": self.entry_nombre.get()}
            self.controller.crear_especialidad(datos)
            messagebox.showinfo("OK", "Especialidad creada.")
            self.cargar()
            self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def actualizar(self):
        try:
            if not hasattr(self, 'selected_id') or self.selected_id is None:
                 raise ValueError("Seleccione una especialidad de la tabla para actualizar.")
            datos = {"nombre": self.entry_nombre.get()}
            self.controller.actualizar_especialidad(self.selected_id, datos)
            messagebox.showinfo("OK", "Especialidad actualizada.")
            self.cargar()
            self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        try:
            if not hasattr(self, 'selected_id') or self.selected_id is None:
                 raise ValueError("Seleccione una especialidad de la tabla para eliminar.")
            if messagebox.askyesno("Confirmar", "¿Eliminar especialidad?"):
                self.controller.eliminar_especialidad(self.selected_id)
                messagebox.showinfo("OK", "Especialidad eliminada.")
                self.cargar()
                self.limpiar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def seleccionar(self, event):
        item = self.tabla.focus()
        vals = self.tabla.item(item, "values")
        if not vals:
            return

        self.selected_id = vals[0]
        self.entry_nombre.delete(0, tk.END)
        self.entry_nombre.insert(0, vals[1])

    def limpiar(self):
        self.entry_nombre.delete(0, tk.END)
        self.selected_id = None