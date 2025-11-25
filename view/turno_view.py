import tkinter as tk
from tkinter import ttk, messagebox
from controller.turno_controller import TurnoController


class TurnoView(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.controller = TurnoController()
        self.turnos_cache = {}
        self.estado_por_nombre = {}
        self.pacientes_display_to_id = {}
        self.pacientes_id_to_display = {}
        self.medicos_display_to_id = {}
        self.medicos_id_to_display = {}
        self.selected_id = None
        self.pack(fill="both", expand=True)

        self._crear_widgets()
        self._cargar_pacientes()
        self._cargar_medicos()
        self._cargar_estados()
        self._cargar_turnos()
        self._limpiar_formulario()

    def _crear_widgets(self):
        form_frame = ttk.LabelFrame(self, text="📝 Registro de Turnos")
        form_frame.pack(fill="x", padx=15, pady=15)

        # Frame interno para controlar el grid
        form_grid = tk.Frame(form_frame)
        form_grid.pack(padx=10, pady=5)
        
        # --- FILA 0: PACIENTE y MÉDICO ---
        tk.Label(form_grid, text="Paciente:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.combo_paciente = ttk.Combobox(form_grid, state="readonly", width=35) # Ancho ajustado
        self.combo_paciente.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(form_grid, text="Médico:").grid(row=0, column=2, sticky="w", padx=20, pady=5)
        self.combo_medico = ttk.Combobox(form_grid, state="readonly", width=35)
        self.combo_medico.grid(row=0, column=3, padx=5, pady=5)

        # --- FILA 1: FECHA y HORA ---
        tk.Label(form_grid, text="Fecha (YYYY-MM-DD):").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.entry_fecha = ttk.Entry(form_grid, width=35) # Usamos ttk.Entry
        self.entry_fecha.grid(row=1, column=1, padx=5, pady=5)

        tk.Label(form_grid, text="Hora (HH:MM):").grid(row=1, column=2, sticky="w", padx=20, pady=5)
        self.entry_hora = ttk.Entry(form_grid, width=35) # Usamos ttk.Entry
        self.entry_hora.grid(row=1, column=3, padx=5, pady=5)

        # --- FILA 2: ESTADO y MOTIVO ---
        tk.Label(form_grid, text="Estado:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.combo_estado = ttk.Combobox(form_grid, state="readonly", width=35)
        self.combo_estado.grid(row=2, column=1, padx=5, pady=5)

        tk.Label(form_grid, text="Motivo:").grid(row=2, column=2, sticky="w", padx=20, pady=5)
        self.entry_motivo = ttk.Entry(form_grid, width=35)
        self.entry_motivo.grid(row=2, column=3, padx=5, pady=5)

        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", padx=15, pady=10)
        

        center_frame = tk.Frame(btn_frame)
        center_frame.pack(anchor="center") 

        ttk.Button(center_frame, text="Guardar", command=self._guardar_turno, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Actualizar", command=self._actualizar_turno, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Eliminar", command=self._eliminar_turno, style='TButton').pack(side="left", padx=5)
        ttk.Button(center_frame, text="Limpiar", command=self._limpiar_formulario, style='TButton').pack(side="left", padx=5)

        # --- TABLA ---
        tabla_frame = tk.Frame(self)
        tabla_frame.pack(fill="both", expand=True, padx=15, pady=10) # Mayor padding

        columnas = ("id", "paciente", "medico", "fecha", "hora", "estado", "motivo")
        self.tabla = ttk.Treeview(tabla_frame, columns=columnas, show="headings", height=12)

        # Configuración de Encabezados
        self.tabla.heading("id", text="ID")
        self.tabla.heading("paciente", text="Paciente")
        self.tabla.heading("medico", text="Médico")
        self.tabla.heading("fecha", text="Fecha")
        self.tabla.heading("hora", text="Hora")
        self.tabla.heading("estado", text="Estado")
        self.tabla.heading("motivo", text="Motivo")

        # Configuración de Columnas
        self.tabla.column("id", width=50, anchor="center")
        self.tabla.column("paciente", width=200, anchor="w")
        self.tabla.column("medico", width=200, anchor="w")
        self.tabla.column("fecha", width=100, anchor="center")
        self.tabla.column("hora", width=80, anchor="center")
        self.tabla.column("estado", width=100, anchor="center")
        self.tabla.column("motivo", width=200, anchor="w")
        
        # Scrollbar
        scrollbar = ttk.Scrollbar(tabla_frame, orient="vertical", command=self.tabla.yview)
        self.tabla.configure(yscrollcommand=scrollbar.set)
        
        scrollbar.pack(side="right", fill="y")
        self.tabla.pack(fill="both", expand=True)
        self.tabla.bind("<<TreeviewSelect>>", self._seleccionar_turno)


    def _cargar_pacientes(self):
        try:
            pacientes = self.controller.listar_pacientes()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            pacientes = []

        self.pacientes_display_to_id = {}
        self.pacientes_id_to_display = {}
        valores = []
        for paciente in pacientes:
            dni = paciente.dni or "-"
            display = (
                f"{paciente.apellido}, {paciente.nombre} - DNI {dni} "
                f"(ID {paciente.id_paciente})"
            )
            self.pacientes_display_to_id[display] = paciente.id_paciente
            self.pacientes_id_to_display[paciente.id_paciente] = display
            valores.append(display)

        self.combo_paciente["values"] = valores
        if not valores:
            self.combo_paciente.set("")

    def _cargar_medicos(self):
        try:
            medicos = self.controller.listar_medicos()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))
            medicos = []

        self.medicos_display_to_id = {}
        self.medicos_id_to_display = {}
        valores = []
        for medico in medicos:
            matricula = medico.matricula or "Sin matricula"
            display = (
                f"{medico.apellido}, {medico.nombre} - Mat {matricula} "
                f"(ID {medico.id_medico})"
            )
            self.medicos_display_to_id[display] = medico.id_medico
            self.medicos_id_to_display[medico.id_medico] = display
            valores.append(display)

        self.combo_medico["values"] = valores
        if not valores:
            self.combo_medico.set("")

    def _cargar_estados(self):
        estados = self.controller.listar_estados()
        self.estado_por_nombre = {estado.nombre: estado.id_estado for estado in estados}
        nombres = list(self.estado_por_nombre.keys())
        self.combo_estado["values"] = nombres
        if nombres:
            self.combo_estado.current(0)

    def _cargar_turnos(self):
        for fila in self.tabla.get_children():
            self.tabla.delete(fila)
        self.turnos_cache.clear()

        turnos = self.controller.listar_turnos()
        for turno in turnos:
            self.turnos_cache[turno.id_turno] = turno
            self.tabla.insert(
                "",
                "end",
                values=(
                    turno.id_turno,
                    f"{turno.paciente_nombre} (ID {turno.id_paciente})",
                    f"{turno.medico_nombre} (ID {turno.id_medico})",
                    turno.fecha,
                    turno.hora,
                    turno.estado_nombre,
                    turno.motivo or "",
                ),
            )

    def _seleccionar_turno(self, _event):
        seleccionado = self.tabla.focus()
        if not seleccionado:
            return

        valores = self.tabla.item(seleccionado, "values")
        if not valores:
            return

        self.selected_id = int(valores[0])
        turno = self.turnos_cache.get(self.selected_id)
        if not turno:
            return

        display_paciente = self.pacientes_id_to_display.get(turno.id_paciente)
        if display_paciente is None:
            self._cargar_pacientes()
            display_paciente = self.pacientes_id_to_display.get(turno.id_paciente)
        if display_paciente:
            self.combo_paciente.set(display_paciente)
        else:
            self.combo_paciente.set("")

        display_medico = self.medicos_id_to_display.get(turno.id_medico)
        if display_medico is None:
            self._cargar_medicos()
            display_medico = self.medicos_id_to_display.get(turno.id_medico)
        if display_medico:
            self.combo_medico.set(display_medico)
        else:
            self.combo_medico.set("")

        self.entry_fecha.delete(0, tk.END)
        self.entry_fecha.insert(0, turno.fecha)

        self.entry_hora.delete(0, tk.END)
        self.entry_hora.insert(0, turno.hora)

        if turno.estado_nombre in self.estado_por_nombre:
            self.combo_estado.set(turno.estado_nombre)

        self.entry_motivo.delete(0, tk.END)
        if turno.motivo:
            self.entry_motivo.insert(0, turno.motivo)

    def _guardar_turno(self):
        try:
            datos = self._obtener_datos_formulario()
            self.controller.registrar_turno(datos)
            messagebox.showinfo("Exito", "Turno guardado correctamente.")
            self._cargar_turnos()
            self._limpiar_formulario()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _actualizar_turno(self):
        try:
            if not hasattr(self, "selected_id") or self.selected_id is None:
                raise ValueError("Seleccione un turno de la tabla.")

            datos = self._obtener_datos_formulario()
            self.controller.actualizar_turno(self.selected_id, datos)
            messagebox.showinfo("Exito", "Turno actualizado correctamente.")
            self._cargar_turnos()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _eliminar_turno(self):
        try:
            if not hasattr(self, "selected_id") or self.selected_id is None:
                raise ValueError("Seleccione un turno de la tabla.")

            if messagebox.askyesno("Confirmar", "Eliminar este turno?"):
                self.controller.eliminar_turno(self.selected_id)
                messagebox.showinfo("Exito", "Turno eliminado.")
                self._cargar_turnos()
                self._limpiar_formulario()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _limpiar_formulario(self):
        self.combo_paciente.set("")
        self.combo_medico.set("")
        self.entry_fecha.delete(0, tk.END)
        self.entry_hora.delete(0, tk.END)
        self.entry_motivo.delete(0, tk.END)
        if self.combo_estado["values"]:
            self.combo_estado.current(0)
        self.selected_id = None

    def _obtener_datos_formulario(self):
        paciente_display = self.combo_paciente.get()
        if not paciente_display:
            raise ValueError("Seleccione un paciente.")

        id_paciente = self.pacientes_display_to_id.get(paciente_display)
        if id_paciente is None:
            raise ValueError("Paciente seleccionado invalido.")

        medico_display = self.combo_medico.get()
        if not medico_display:
            raise ValueError("Seleccione un medico.")

        id_medico = self.medicos_display_to_id.get(medico_display)
        if id_medico is None:
            raise ValueError("Medico seleccionado invalido.")

        estado_nombre = self.combo_estado.get()
        if not estado_nombre:
            raise ValueError("Seleccione un estado.")

        id_estado = self.estado_por_nombre.get(estado_nombre)
        if id_estado is None:
            raise ValueError("Estado invalido.")

        return {
            "id_paciente": str(id_paciente),
            "id_medico": str(id_medico),
            "fecha": self.entry_fecha.get(),
            "hora": self.entry_hora.get(),
            "motivo": self.entry_motivo.get(),
            "id_estado": id_estado,
        }