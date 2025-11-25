import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controller.agenda_controller import AgendaController
from controller.medico_controller import MedicoController

class AgendaView(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.controller = AgendaController()
        self.medico_controller = MedicoController()
        self.dias_map = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        self.medicos_filtrados = []
        self.medicos_por_id = {}
        self.selected_medico_id = None
        self.selected_id_agenda = None
        
        self.var_id_medico = tk.StringVar()
        self.var_nombre_medico = tk.StringVar(value="Sin médico seleccionado")
        
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.buscar_medicos()
        self.selected_id_agenda = None

    def create_widgets(self):
        search = ttk.LabelFrame(self, text="🔍 Buscar médico")
        search.pack(fill="x", padx=15, pady=15)

        search.columnconfigure(0, weight=1) 
        search.columnconfigure(3, weight=1)

        tk.Label(search, text="Nombre o apellido:").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.entry_buscar_medico = ttk.Entry(search, width=30) 
        self.entry_buscar_medico.grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Button(search, text="Buscar", command=self.buscar_medicos, width=10).grid(row=0, column=3, sticky="w", padx=5, pady=5)

        self.lista_medicos = tk.Listbox(search, height=6, width=45, bd=1, relief="flat", bg="#F8F8F8")
        self.lista_medicos.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="we")
        self.lista_medicos.bind("<<ListboxSelect>>", self.seleccionar_medico_lista)

        # -----------------------------------------------------------------
        # SECCIÓN DE GESTIÓN DE AGENDA (Stylized)
        # -----------------------------------------------------------------
        form = ttk.LabelFrame(self, text="🗓️ Gestión de Agenda") 
        form.pack(fill="x", padx=15, pady=10)

        # Frame interno para controlar el grid
        form_grid = tk.Frame(form)
        form_grid.pack(padx=10, pady=5)
        
        # --- FILA 0: IDENTIFICACIÓN Y DÍA ---
        tk.Label(form_grid, text="ID Médico:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_id_medico = ttk.Entry(form_grid, textvariable=self.var_id_medico, state="readonly", width=15)
        self.entry_id_medico.grid(row=0, column=1, padx=5, pady=5)
        
        tk.Label(form_grid, text="Día:").grid(row=0, column=2, sticky="w", padx=20, pady=5)
        self.combo_dia = ttk.Combobox(form_grid, values=self.dias_map, state="readonly", width=15)
        self.combo_dia.grid(row=0, column=3, padx=5, pady=5)
        self.combo_dia.current(0)

        # --- FILA 1: HORARIOS DE TRABAJO ---
        tk.Label(form_grid, text="Hora Inicio (HH:MM):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_hora_desde = ttk.Entry(form_grid, width=15)
        self.entry_hora_desde.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_grid, text="Duración Jornada (Hs):").grid(row=1, column=2, sticky="w", padx=20, pady=5)
        self.entry_duracion_horas = ttk.Entry(form_grid, width=15)
        self.entry_duracion_horas.insert(0, "4")
        self.entry_duracion_horas.grid(row=1, column=3, padx=5, pady=5)

        # --- FILA 2: DURACIÓN DE SLOTS ---
        tk.Label(form_grid, text="Duración Turno (min):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_duracion = ttk.Entry(form_grid, width=15)
        self.entry_duracion.insert(0, "30")
        self.entry_duracion.grid(row=2, column=1, padx=5, pady=5)
        
        tk.Label(form_grid, text="Médico Seleccionado:", fg="#4CAF50").grid(row=3, column=0, sticky="w", padx=5, pady=5, columnspan=2)
        tk.Label(form_grid, textvariable=self.var_nombre_medico, fg="#4CAF50").grid(row=3, column=2, sticky="w", padx=5, pady=5, columnspan=2)


        # --- BOTONES DE ACCIÓN ---
        btns = tk.Frame(self)
        btns.pack(fill="x", padx=15, pady=10)
        
        center_frame = tk.Frame(btns)
        center_frame.pack(anchor="center") 
        
        ttk.Button(center_frame, text="🔍 Buscar Agendas del Médico", command=self.cargar, style='TButton').pack(side="left", padx=5)
        tk.Frame(center_frame, width=20).pack(side="left") # Espacio separador
        ttk.Button(center_frame, text="Guardar", command=self.guardar, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Eliminar", command=self.eliminar, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Limpiar Campos", command=self.limpiar, style='TButton').pack(side="left", padx=5)

        # --- TABLA ---
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10) 

        cols = ("id_agenda", "id_medico", "dia", "desde", "hasta", "duracion")
        self.tabla = ttk.Treeview(table_frame, columns=cols, show="headings")
        

        self.tabla.heading("id_agenda", text="ID Agenda", command=lambda c="id_agenda": self.ordenar_columna(c, False))
        self.tabla.heading("id_medico", text="ID Médico", command=lambda c="id_medico": self.ordenar_columna(c, False))
        self.tabla.heading("dia", text="Día", command=lambda c="dia": self.ordenar_columna(c, False))
        self.tabla.heading("desde", text="Inicio (HH:MM)", command=lambda c="desde": self.ordenar_columna(c, False))
        self.tabla.heading("hasta", text="Fin (HH:MM)", command=lambda c="hasta": self.ordenar_columna(c, False))
        self.tabla.heading("duracion", text="Slot (min)", command=lambda c="duracion": self.ordenar_columna(c, False))
        
        # Configuración de Columnas
        self.tabla.column("id_agenda", width=70, anchor="center")
        self.tabla.column("id_medico", width=80, anchor="center")
        self.tabla.column("dia", width=100, anchor="w")
        self.tabla.column("desde", width=100, anchor="center")
        self.tabla.column("hasta", width=100, anchor="center")
        self.tabla.column("duracion", width=80, anchor="center")

        # Scrollbar para la tabla
        scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    # -------------------------------------------
    # Ordenar columnas 
    # -------------------------------------------
    def ordenar_columna(self, col, reverse):
        l = [(self.tabla.set(k, col), k) for k in self.tabla.get_children('')]
        
        try:
            l.sort(key=lambda t: int(t[0]), reverse=reverse)
        except ValueError:
            l.sort(key=lambda t: t[0].lower(), reverse=reverse)

        for index, (val, k) in enumerate(l):
            self.tabla.move(k, '', index)

        self.tabla.heading(col, command=lambda: self.ordenar_columna(col, not reverse))


    def cargar(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        if not self.selected_medico_id:
            messagebox.showwarning("Aviso", "Seleccione un médico de la lista.")
            return

        try:
            agendas = self.controller.obtener_agendas_medico(self.selected_medico_id)
            for a in agendas:
                nombre_dia = self.dias_map[a.dia_semana]
                self.tabla.insert("", "end", values=(
                    a.id_agenda, a.id_medico, nombre_dia,
                    a.hora_desde, a.hora_hasta, a.duracion_turno_min
                ))
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def guardar(self):
        try:
            idx_dia = self.combo_dia.current()
            if idx_dia < 0: idx_dia = 0

            if not self.selected_medico_id:
                raise ValueError("Debe seleccionar un médico.")

            datos = {
                "id_medico": self.selected_medico_id,
                "dia_semana": idx_dia,
                "hora_desde": self.entry_hora_desde.get(),
                "duracion_horas": self.entry_duracion_horas.get(),
                "duracion_turno_min": self.entry_duracion.get()
            }
            
            self.controller.crear_agenda(datos)
            messagebox.showinfo("OK", "Agenda creada exitosamente.")
            self.cargar()
            
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def seleccionar(self, event):
        item = self.tabla.focus()
        vals = self.tabla.item(item, "values")
        if not vals: return

        self.selected_id_agenda = vals[0]

        try:
            medico_id = int(vals[1])
        except (TypeError, ValueError):
            medico_id = None

        if medico_id:
            self.establecer_medico(medico_id)

        if vals[2] in self.dias_map:
            self.combo_dia.set(vals[2])

        self.entry_hora_desde.delete(0, tk.END)
        self.entry_hora_desde.insert(0, vals[3])

        try:
            fmt = "%H:%M"
            t1 = datetime.strptime(vals[3], fmt) 
            t2 = datetime.strptime(vals[4], fmt) 
            diff = t2 - t1
            horas = diff.total_seconds() / 3600
            
            self.entry_duracion_horas.delete(0, tk.END)
            self.entry_duracion_horas.insert(0, f"{horas:g}")
        except:
            self.entry_duracion_horas.delete(0, tk.END)

        self.entry_duracion.delete(0, tk.END)
        self.entry_duracion.insert(0, vals[5])

    def limpiar(self):
        self.entry_buscar_medico.delete(0, tk.END)
        self.lista_medicos.selection_clear(0, tk.END)
        self.medicos_filtrados = []
        self.selected_medico_id = None
        self.var_id_medico.set("")
        self.var_nombre_medico.set("Sin médico seleccionado")
        self.entry_hora_desde.delete(0, tk.END)
        self.entry_duracion_horas.delete(0, tk.END)
        self.entry_duracion.delete(0, tk.END)
        self.entry_duracion.insert(0, "30")
        self.combo_dia.current(0)
        self.selected_id_agenda = None
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        self.buscar_medicos()

    def eliminar(self):
        if not self.selected_id_agenda:
            messagebox.showwarning("Aviso", "Seleccione una agenda de la lista para eliminar.")
            return

        confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de eliminar este horario de la agenda?")
        if confirmacion:
            try:
                self.controller.eliminar_agenda(self.selected_id_agenda)
                messagebox.showinfo("Éxito", "Horario eliminado correctamente.")
            
                self.cargar() 
                self.limpiar() 
                
            except Exception as e:
                messagebox.showerror("Error", f"No se pudo eliminar: {str(e)}")

    def buscar_medicos(self):
        termino = self.entry_buscar_medico.get().strip().lower()
        medicos = self.medico_controller.listar_medicos()
        self.medicos_por_id = {med.id_medico: med for med in medicos}

        if termino:
            medicos = [m for m in medicos if termino in m.nombre.lower() or termino in m.apellido.lower()]

        self.medicos_filtrados = medicos
        self.lista_medicos.delete(0, tk.END)

        for med in medicos:
            texto = f"{med.id_medico} - {med.apellido}, {med.nombre}"
            self.lista_medicos.insert(tk.END, texto)

    def seleccionar_medico_lista(self, _event):
        if not self.lista_medicos.curselection():
            return

        idx = self.lista_medicos.curselection()[0]
        if idx < 0 or idx >= len(self.medicos_filtrados):
            return

        medico = self.medicos_filtrados[idx]
        self.establecer_medico(medico.id_medico)

    def establecer_medico(self, id_medico):
        medico = self.medicos_por_id.get(id_medico)
        if medico is None:
            try:
                todos = self.medico_controller.listar_medicos()
                self.medicos_por_id = {med.id_medico: med for med in todos}
                medico = self.medicos_por_id.get(id_medico)
            except Exception:
                medico = None

        self.selected_medico_id = id_medico
        self.var_id_medico.set(str(id_medico))

        if medico:
            self.var_nombre_medico.set(f"{medico.apellido}, {medico.nombre}")
        else:
            self.var_nombre_medico.set("Médico seleccionado")

        # sincronizar selección del listbox si el médico está visible
        for idx, med in enumerate(self.medicos_filtrados):
            if med.id_medico == id_medico:
                self.lista_medicos.selection_clear(0, tk.END)
                self.lista_medicos.selection_set(idx)
                self.lista_medicos.see(idx)
                break