import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime

from controller.historia_clinica_controller import HistoriaClinicaController


class HistoriaClinicaView(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.controller = HistoriaClinicaController()
        self.pacientes = []
        self.pacientes_filtrados = []
        self.turnos_actuales = []
        self.historia_actual = []
        self.historia_map = {}
        self.selected_paciente_id = None
        self.selected_turno_id = None
        
        self.var_paciente_info = tk.StringVar(value="Sin paciente seleccionado")

        self.pack(fill="both", expand=True)
        
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas) # Contenedor real para todos los widgets

        
        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        self.canvas.bind('<Configure>', lambda e: self.canvas.configure(scrollregion = self.canvas.bbox("all")))
        
   
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")


        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        self._crear_widgets(self.scrollable_frame) 
        
        
        self._limpiar_formulario()
        self._limpiar_detalle()
        self._cargar_pacientes()

    def _crear_widgets(self, parent_frame):
        
        # -----------------------------------------------------------------
        # 1. SECCIÓN DE BÚSQUEDA DE PACIENTE 
        # -----------------------------------------------------------------
        search_frame = ttk.LabelFrame(parent_frame, text="🔍 Buscar paciente")
        search_frame.pack(fill="x", padx=15, pady=15)

        search_frame.columnconfigure(0, weight=1) 
        search_frame.columnconfigure(3, weight=1)

        tk.Label(search_frame, text="Nombre, apellido o DNI:").grid(row=0, column=1, sticky="w", padx=5, pady=5)
        self.entry_buscar_paciente = ttk.Entry(search_frame, width=30) 
        self.entry_buscar_paciente.grid(row=0, column=2, padx=5, pady=5)
        
        ttk.Button(search_frame, text="Buscar", command=self._filtrar_pacientes, style='TButton').grid(row=0, column=3, sticky="w", padx=5, pady=5) 

        self.lista_pacientes = tk.Listbox(search_frame, height=6, width=50, bd=1, relief="flat", bg="#F8F8F8")
        self.lista_pacientes.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="we")
        self.lista_pacientes.bind("<<ListboxSelect>>", self._seleccionar_paciente_lista)

        # Información del paciente seleccionado
        tk.Label(parent_frame, textvariable=self.var_paciente_info, font=("Arial", 11, "bold"), fg="#4CAF50", anchor="w").pack(fill="x", padx=15, pady=(5, 10))

        # -----------------------------------------------------------------
        # 2. TABLA DE TURNOS
        # -----------------------------------------------------------------
        turnos_frame = ttk.LabelFrame(parent_frame, text="📋 Turnos del paciente (Pendientes/Atendidos)")
        turnos_frame.pack(fill="x", padx=15, pady=10)

        columnas_turnos = ("fecha", "hora", "medico", "estado", "motivo")
        self.tabla_turnos = ttk.Treeview(turnos_frame, columns=columnas_turnos, show="headings", height=6)
        
        for col, titulo in zip(columnas_turnos, ["Fecha", "Hora", "Médico", "Estado", "Motivo"]):
            self.tabla_turnos.heading(col, text=titulo)
            ancho = 110 if col in ("fecha", "hora", "estado") else 160
            self.tabla_turnos.column(col, width=ancho, anchor="center")
        self.tabla_turnos.column("motivo", width=180, anchor="w")
        
        ttk.Scrollbar(turnos_frame, orient="vertical", command=self.tabla_turnos.yview).pack(side="right", fill="y")
        self.tabla_turnos.pack(fill="both", expand=True)
        self.tabla_turnos.bind("<<TreeviewSelect>>", self._seleccionar_turno)

        # -----------------------------------------------------------------
        # 3. FORMULARIO DE REGISTRO DE ATENCIÓN
        # -----------------------------------------------------------------
        form_atencion = ttk.LabelFrame(parent_frame, text="✍️ Registrar atención")
        form_atencion.pack(fill="x", padx=15, pady=10)

        left = tk.Frame(form_atencion)
        left.grid(row=0, column=0, sticky="nsew", padx=5, pady=5)

        right = tk.Frame(form_atencion)
        right.grid(row=0, column=1, sticky="nsew", padx=10, pady=5)

        form_atencion.grid_columnconfigure(0, weight=3) 
        form_atencion.grid_columnconfigure(1, weight=1) 
        form_atencion.grid_rowconfigure(0, weight=1)

        # ===== IZQUIERDA (Campos de atención) =====
        tk.Label(left, text="Fecha historia (YYYY-MM-DD):").grid(row=0, column=0, sticky="w", padx=5)
        self.entry_fecha_historia = ttk.Entry(left, width=15) # Usamos ttk.Entry
        self.entry_fecha_historia.grid(row=0, column=1, sticky="w", pady=5)

        tk.Label(left, text="Diagnostico:").grid(row=1, column=0, sticky="nw", padx=5)
        self.txt_diagnostico = tk.Text(left, width=50, height=3) 
        self.txt_diagnostico.grid(row=1, column=1, pady=5)

        tk.Label(left, text="Procedimiento:").grid(row=2, column=0, sticky="nw", padx=5)
        self.txt_procedimiento = tk.Text(left, width=50, height=3)
        self.txt_procedimiento.grid(row=2, column=1, pady=5)

        tk.Label(left, text="Indicaciones:").grid(row=3, column=0, sticky="nw", padx=5)
        self.txt_indicaciones = tk.Text(left, width=50, height=3)
        self.txt_indicaciones.grid(row=3, column=1, pady=5)

        tk.Label(left, text="Resumen historia:").grid(row=4, column=0, sticky="nw", padx=5)
        self.txt_resumen = tk.Text(left, width=50, height=3)
        self.txt_resumen.grid(row=4, column=1, pady=5)

        # ===== DERECHA (Botones de acción) =====
        right_btn_frame = tk.Frame(right)
        right_btn_frame.pack(anchor="center", expand=True)

        self.btn_guardar = ttk.Button(right_btn_frame, text="Guardar atención", width=20, command=self._guardar_atencion, style='TButton')
        self.btn_guardar.pack(fill="x", pady=10)

        self.btn_limpiar = ttk.Button(right_btn_frame, text="Limpiar", width=20, command=self._limpiar_formulario, style='TButton')
        self.btn_limpiar.pack(fill="x", pady=5)


        historia_frame = ttk.LabelFrame(parent_frame, text="📜 Historia Clínica")
        historia_frame.pack(fill="x", padx=15, pady=10) 

        columnas_historia = ("fecha", "turno", "medico", "diagnostico", "resumen")
        self.tabla_historia = ttk.Treeview(historia_frame, columns=columnas_historia, show="headings", height=6)

        titulos_historia = ["Fecha", "Turno", "Médico", "Diagnóstico", "Resumen"]
        for col, titulo in zip(columnas_historia, titulos_historia):
            self.tabla_historia.heading(col, text=titulo)
            ancho = 110 if col == "fecha" else 180
            if col == "turno":
                ancho = 140
            self.tabla_historia.column(col, width=ancho, anchor="center")
        self.tabla_historia.column("diagnostico", width=220, anchor="w")
        self.tabla_historia.column("resumen", width=260, anchor="w")

        ttk.Scrollbar(historia_frame, orient="vertical", command=self.tabla_historia.yview).pack(side="right", fill="y")
        self.tabla_historia.pack(fill="both", expand=True)
        self.tabla_historia.bind("<<TreeviewSelect>>", self._mostrar_historia_detalle)

        # -----------------------------------------------------------------
        # 5. DETALLE DE LA ATENCIÓN 
        # -----------------------------------------------------------------
        detalle_frame = ttk.LabelFrame(parent_frame, text="📋 Detalle de la Atención")
        detalle_frame.pack(fill="x", padx=15, pady=10) 
        
        detalle_grid = tk.Frame(detalle_frame)
        detalle_grid.pack(padx=10, pady=5)

        # Diagnostico
        tk.Label(detalle_grid, text="Diagnóstico:").grid(row=0, column=0, sticky="w", padx=5, pady=5)
        self.txt_det_diagnostico = tk.Text(detalle_grid, width=60, height=3)
        self.txt_det_diagnostico.grid(row=0, column=1, padx=5, pady=5)

        # Procedimiento
        tk.Label(detalle_grid, text="Procedimiento:").grid(row=1, column=0, sticky="w", padx=5, pady=5)
        self.txt_det_procedimiento = tk.Text(detalle_grid, width=60, height=3)
        self.txt_det_procedimiento.grid(row=1, column=1, padx=5, pady=5)

        # Indicaciones
        tk.Label(detalle_grid, text="Indicaciones:").grid(row=2, column=0, sticky="w", padx=5, pady=5)
        self.txt_det_indicaciones = tk.Text(detalle_grid, width=60, height=3)
        self.txt_det_indicaciones.grid(row=2, column=1, padx=5, pady=5)

        # Resumen
        tk.Label(detalle_grid, text="Resumen:").grid(row=3, column=0, sticky="w", padx=5, pady=5)
        self.txt_det_resumen = tk.Text(detalle_grid, width=60, height=3)
        self.txt_det_resumen.grid(row=3, column=1, padx=5, pady=5)

        self.form_textos = [self.txt_diagnostico, self.txt_procedimiento, self.txt_indicaciones, self.txt_resumen]
        self.detalle_textos = [self.txt_det_diagnostico, self.txt_det_procedimiento, self.txt_det_indicaciones, self.txt_det_resumen]

        for txt in self.detalle_textos:
            txt.configure(state="disabled")

    def _cargar_pacientes(self):
        try:
            self.pacientes = self.controller.listar_pacientes()
            self._filtrar_pacientes()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _filtrar_pacientes(self):
        termino = self.entry_buscar_paciente.get().strip().lower()
        if termino:
            filtrados = [
                p for p in self.pacientes
                if termino in p.nombre.lower()
                or termino in p.apellido.lower()
                or termino in (p.dni or "").lower()
            ]
        else:
            filtrados = list(self.pacientes)

        self.pacientes_filtrados = filtrados
        self.lista_pacientes.delete(0, tk.END)
        for paciente in filtrados:
            texto = f"{paciente.id_paciente} - {paciente.apellido}, {paciente.nombre} (DNI {paciente.dni})"
            self.lista_pacientes.insert(tk.END, texto)

    def _seleccionar_paciente_lista(self, _event):
        if not self.lista_pacientes.curselection():
            return
        idx = self.lista_pacientes.curselection()[0]
        if idx < 0 or idx >= len(self.pacientes_filtrados):
            return

        paciente = self.pacientes_filtrados[idx]
        self.selected_paciente_id = paciente.id_paciente
        self.var_paciente_info.set(
            f"Paciente seleccionado: {paciente.apellido}, {paciente.nombre} (DNI {paciente.dni})"
        )
        self._limpiar_formulario()
        self._limpiar_detalle()
        self.historia_actual = []
        self._cargar_turnos()
        self._cargar_historia()

    def _cargar_turnos(self):
        for fila in self.tabla_turnos.get_children():
            self.tabla_turnos.delete(fila)
        self.turnos_actuales = []
        self.selected_turno_id = None

        if not self.selected_paciente_id:
            return

        try:
            turnos = self.controller.listar_turnos_paciente(self.selected_paciente_id)
            self.turnos_actuales = turnos
            for turno in turnos:
                self.tabla_turnos.insert(
                    "",
                    "end",
                    iid=str(turno.id_turno),
                    values=(
                        turno.fecha,
                        turno.hora,
                        turno.medico_nombre,
                        turno.estado_nombre,
                        turno.motivo or "",
                    ),
                )
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _seleccionar_turno(self, _event):
        if not self.tabla_turnos.selection():
            return
        item = self.tabla_turnos.selection()[0]
        try:
            turno_id = int(item)
        except ValueError:
            return

        self.selected_turno_id = turno_id
        self._cargar_atencion(turno_id)

    def _cargar_atencion(self, turno_id):
        self._limpiar_formulario_campos()
        self.selected_turno_id = turno_id

        try:
            atencion = self.controller.obtener_atencion_por_turno(turno_id)
            if not atencion:
                return

            if atencion.diagnostico:
                self.txt_diagnostico.insert(tk.END, atencion.diagnostico)
            if atencion.procedimiento:
                self.txt_procedimiento.insert(tk.END, atencion.procedimiento)
            if atencion.indicaciones:
                self.txt_indicaciones.insert(tk.END, atencion.indicaciones)

            historia_relacionada = None
            if atencion.id_atencion:
                for historia in self.historia_actual:
                    if historia.id_atencion == atencion.id_atencion:
                        historia_relacionada = historia
                        break
            
            if historia_relacionada:
                self.entry_fecha_historia.delete(0, tk.END)
                self.entry_fecha_historia.insert(0, historia_relacionada.fecha)
                if historia_relacionada.resumen:
                    self.txt_resumen.insert(tk.END, historia_relacionada.resumen)
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _guardar_atencion(self):
        if not self.selected_paciente_id:
            messagebox.showwarning("Aviso", "Seleccione un paciente.")
            return
        if not self.selected_turno_id:
            messagebox.showwarning("Aviso", "Seleccione un turno.")
            return

        datos = {
            "id_paciente": self.selected_paciente_id,
            "id_turno": self.selected_turno_id,
            "fecha": self.entry_fecha_historia.get().strip(),
            "diagnostico": self.txt_diagnostico.get("1.0", tk.END).strip(),
            "procedimiento": self.txt_procedimiento.get("1.0", tk.END).strip(),
            "indicaciones": self.txt_indicaciones.get("1.0", tk.END).strip(),
            "resumen": self.txt_resumen.get("1.0", tk.END).strip(),
        }

        try:
            self.controller.registrar_atencion(datos)
            messagebox.showinfo("Exito", "Atencion registrada correctamente.")
            self._cargar_turnos()
            self._cargar_historia()
            self._limpiar_formulario()
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _limpiar_formulario_campos(self):
        self.entry_fecha_historia.delete(0, tk.END)
        self.entry_fecha_historia.insert(0, datetime.now().strftime("%Y-%m-%d"))
        for widget in self.form_textos:
            widget.delete("1.0", tk.END)

    def _limpiar_formulario(self):
        self._limpiar_formulario_campos()
        self.selected_turno_id = None
        for item in self.tabla_turnos.selection():
            self.tabla_turnos.selection_remove(item)

    def _cargar_historia(self):
        for fila in self.tabla_historia.get_children():
            self.tabla_historia.delete(fila)
        self.historia_map = {}
        self._limpiar_detalle()

        if not self.selected_paciente_id:
            return

        try:
            historias = self.controller.obtener_historia_paciente(self.selected_paciente_id)
            self.historia_actual = historias or []
            for idx, historia in enumerate(self.historia_actual):
                turno_info = "-"
                if historia.turno_fecha and historia.turno_hora:
                    turno_info = f"{historia.turno_fecha} {historia.turno_hora}"
                
                iid = str(historia.id_historia) if historia.id_historia is not None else f"temp_{idx}"
                
                self.tabla_historia.insert(
                    "",
                    "end",
                    iid=iid,
                    values=(
                        historia.fecha,
                        turno_info,
                        historia.medico_nombre or "-",
                        historia.diagnostico or "",
                        historia.resumen,
                    ),
                )
                self.historia_map[iid] = historia
        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _mostrar_historia_detalle(self, _event):
        if not self.tabla_historia.selection():
            return

        iid = self.tabla_historia.selection()[0]
        historia = self.historia_map.get(iid)
        if historia is None:
            return
        self._limpiar_detalle()

        self._set_text(self.txt_det_diagnostico, historia.diagnostico)
        self._set_text(self.txt_det_procedimiento, historia.procedimiento)
        self._set_text(self.txt_det_indicaciones, historia.indicaciones)
        self._set_text(self.txt_det_resumen, historia.resumen)

    def _limpiar_detalle(self):
        for txt in self.detalle_textos:
            txt.configure(state="normal")
            txt.delete("1.0", tk.END)
            txt.configure(state="disabled")

    def _set_text(self, widget, contenido):
        widget.configure(state="normal")
        if contenido:
            widget.insert(tk.END, contenido)
        widget.configure(state="disabled")