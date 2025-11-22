# view/especialidad_view.py

import tkinter as tk
from tkinter import ttk, messagebox
from controller.especialidad_controller import EspecialidadController

class EspecialidadView(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.controller = EspecialidadController()
        self.pack(fill="both", expand=True)

        self.create_widgets()
        self.cargar()

    # -----------------------------
    # UI
    # -----------------------------
    def create_widgets(self):
        form = tk.LabelFrame(self, text="Especialidad")
        form.pack(fill="x", padx=10, pady=10)

        tk.Label(form, text="Nombre:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_nombre = tk.Entry(form)
        self.entry_nombre.grid(row=0, column=1, padx=5, pady=5)

        # Botones
        btns = tk.Frame(self)
        btns.pack(fill="x", padx=10, pady=10)

        tk.Button(btns, text="Guardar", command=self.guardar).pack(side="left", padx=5)
        tk.Button(btns, text="Actualizar", command=self.actualizar).pack(side="left", padx=5)
        tk.Button(btns, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        tk.Button(btns, text="Limpiar", command=self.limpiar).pack(side="left", padx=5)

        # Tabla
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("id", "nombre")
        self.tabla = ttk.Treeview(table_frame, columns=cols, show="headings")

        self.tabla.heading("id", text="ID")
        self.tabla.heading("nombre", text="Nombre")

        self.tabla.column("id", width=60)
        self.tabla.column("nombre", width=200)

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
            datos = {"nombre": self.entry_nombre.get()}
            self.controller.actualizar_especialidad(self.selected_id, datos)
            messagebox.showinfo("OK", "Especialidad actualizada.")
            self.cargar()
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def eliminar(self):
        try:
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
