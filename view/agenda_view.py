import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from controller.agenda_controller import AgendaController

class AgendaView(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.controller = AgendaController()
        self.dias_map = ["Lunes", "Martes", "Miércoles", "Jueves", "Viernes", "Sábado", "Domingo"]
        
        self.pack(fill="both", expand=True)
        self.create_widgets()
        self.selected_id_agenda = None

    def create_widgets(self):
        form = tk.LabelFrame(self, text="Gestión de Agenda")
        form.pack(fill="x", padx=10, pady=10)

        # ID Médico
        tk.Label(form, text="ID Médico:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.entry_id_medico = tk.Entry(form)
        self.entry_id_medico.grid(row=0, column=1, padx=5, pady=5)

        # Día
        tk.Label(form, text="Día:").grid(row=0, column=2, sticky="w", padx=5, pady=5)
        self.combo_dia = ttk.Combobox(form, values=self.dias_map, state="readonly")
        self.combo_dia.grid(row=0, column=3, padx=5, pady=5)
        self.combo_dia.current(0)

        # Hora Desde
        tk.Label(form, text="Hora Inicio (HH:MM):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_hora_desde = tk.Entry(form)
        self.entry_hora_desde.grid(row=1, column=1, padx=5, pady=5)

        # --- CAMBIO AQUÍ: Duración Jornada ---
        tk.Label(form, text="Duración Jornada (Hs):").grid(row=1, column=2, sticky="w", padx=5, pady=5)
        self.entry_duracion_horas = tk.Entry(form)
        self.entry_duracion_horas.insert(0, "4") # Valor por defecto sugerido
        self.entry_duracion_horas.grid(row=1, column=3, padx=5, pady=5)

        # Duración Turno (Slots)
        tk.Label(form, text="Duración Turno (min):").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.entry_duracion = tk.Entry(form)
        self.entry_duracion.insert(0, "30")
        self.entry_duracion.grid(row=2, column=1, padx=5, pady=5)

        # Botones
        btns = tk.Frame(self)
        btns.pack(fill="x", padx=10, pady=10)
        tk.Button(btns, text="🔍 Buscar Agendas del Médico", command=self.cargar).pack(side="left", padx=5)
        tk.Frame(btns, width=20).pack(side="left")
        tk.Button(btns, text="Guardar", command=self.guardar).pack(side="left", padx=5)
        tk.Button(btns, text="Eliminar", command=self.eliminar).pack(side="left", padx=5)
        tk.Button(btns, text="Limpiar Campos", command=self.limpiar).pack(side="left", padx=5)

        # Tabla
        table_frame = tk.Frame(self)
        table_frame.pack(fill="both", expand=True, padx=10, pady=10)

        cols = ("id_agenda", "id_medico", "dia", "desde", "hasta", "duracion")
        self.tabla = ttk.Treeview(table_frame, columns=cols, show="headings")
        self.tabla.heading("id_agenda", text="ID")
        self.tabla.heading("id_medico", text="Médico")
        self.tabla.heading("dia", text="Día")
        self.tabla.heading("desde", text="Inicio")
        self.tabla.heading("hasta", text="Fin")
        self.tabla.heading("duracion", text="Slot (min)")
        
        for col in cols:
            self.tabla.column(col, width=80)

        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self.seleccionar)

    def cargar(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

        id_medico = self.entry_id_medico.get()
        if not id_medico: return

        try:
            agendas = self.controller.obtener_agendas_medico(id_medico)
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

            datos = {
                "id_medico": self.entry_id_medico.get(),
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
        self.entry_id_medico.delete(0, tk.END)
        self.entry_id_medico.insert(0, vals[1])

        if vals[2] in self.dias_map:
            self.combo_dia.set(vals[2])

        self.entry_hora_desde.delete(0, tk.END)
        self.entry_hora_desde.insert(0, vals[3])

        try:
            fmt = "%H:%M"
            t1 = datetime.strptime(vals[3], fmt) # Inicio
            t2 = datetime.strptime(vals[4], fmt) # Fin
            diff = t2 - t1
            horas = diff.total_seconds() / 3600
            
            self.entry_duracion_horas.delete(0, tk.END)
            self.entry_duracion_horas.insert(0, f"{horas:g}")
        except:
            self.entry_duracion_horas.delete(0, tk.END)

        self.entry_duracion.delete(0, tk.END)
        self.entry_duracion.insert(0, vals[5])

    def limpiar(self):
        self.entry_id_medico.delete(0, tk.END)
        self.entry_hora_desde.delete(0, tk.END)
        self.entry_duracion_horas.delete(0, tk.END)
        self.entry_duracion.delete(0, tk.END)
        self.entry_duracion.insert(0, "30")
        self.combo_dia.current(0)
        self.selected_id_agenda = None
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)

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