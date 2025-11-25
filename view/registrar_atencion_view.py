import tkinter as tk
from tkinter import ttk, messagebox
from datetime import datetime
from tkinter import filedialog 

from controller.historia_clinica_controller import HistoriaClinicaController


class RegistrarAtencionView(tk.Frame):

    def __init__(self, master):
        super().__init__(master)
        self.controller = HistoriaClinicaController()
        self.pacientes = []
        self.pacientes_filtrados = []
        self.turnos_actuales = []
        self.selected_paciente_id = None
        self.selected_turno_id = None
        
        self.var_paciente_info = tk.StringVar(value="Sin paciente seleccionado")

        self.pack(fill="both", expand=True)
        
        # --- IMPLEMENTACIÓN DEL SCROLLBAR ---
        self.canvas = tk.Canvas(self)
        self.scrollbar = ttk.Scrollbar(self, orient="vertical", command=self.canvas.yview)
        self.scrollable_frame = tk.Frame(self.canvas)

        self.canvas.configure(yscrollcommand=self.scrollbar.set)
        # Asegura que el scrollregion se ajuste al tamaño del frame contenido
        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion = self.canvas.bbox("all")
            )
        )
        
        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.scrollbar.pack(side="right", fill="y")
        self.canvas.pack(side="left", fill="both", expand=True)
        
        # Ejecutar la creación de widgets dentro del frame desplazable
        self._crear_widgets(self.scrollable_frame) 
        
        self._limpiar_formulario()
        self._cargar_pacientes()

    def _crear_widgets(self, parent_frame):
        # -----------------------------------------------------------------
        # 1. SECCIÓN DE BÚSQUEDA DE PACIENTE (Stylized)
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
        self.entry_fecha_historia = ttk.Entry(left, width=15) 
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

        self.form_textos = [self.txt_diagnostico, self.txt_procedimiento, self.txt_indicaciones, self.txt_resumen]

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
        self._cargar_turnos()

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

            # Intentamos buscar si ya hay historia para poner la fecha y resumen
            # Esto es un poco hacky porque no tenemos la historia directa desde atencion en el controller
            # pero podemos inferirlo o dejarlo vacio si es edicion.
            # Por ahora solo cargamos lo de atencion.
            
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
            historia, _ = self.controller.registrar_atencion(datos)
            
            if messagebox.askyesno("Atención Guardada", "Atención registrada correctamente.\n\n¿Desea generar una receta electrónica?"):
                self._abrir_modal_receta(historia)
            else:
                self._cargar_turnos()
                self._limpiar_formulario()

        except Exception as exc:
            messagebox.showerror("Error", str(exc))

    def _abrir_modal_receta(self, historia):
        modal = tk.Toplevel(self)
        modal.title("Generar Receta Electrónica")
        modal.geometry("500x400")
        modal.resizable(False, False)

        tk.Label(modal, text="Detalle de la prescripción:", font=("Arial", 10, "bold")).pack(anchor="w", padx=10, pady=10)
        
        txt_receta = tk.Text(modal, height=10)
        txt_receta.insert("1.0", self.txt_indicaciones.get("1.0", tk.END).strip())
        txt_receta.pack(fill="both", expand=True, padx=10, pady=5)

        try:
            receta_existente = self.controller.receta_service.obtener_por_atencion(historia.id_atencion)
            if receta_existente:
                txt_receta.insert("1.0", receta_existente.detalle)
        except:
            pass

        def _guardar_receta():
            diagnostico = self.txt_diagnostico.get("1.0", tk.END).strip() 
            detalle = txt_receta.get("1.0", tk.END).strip()
            if not detalle:
                messagebox.showwarning("Aviso", "El detalle de la receta no puede estar vacío.", parent=modal)
                return
            
            try:
                receta = self.controller.crear_receta(historia.id_atencion, detalle, historia.fecha, diagnostico)
                
                if messagebox.askyesno("Receta Guardada", "Receta generada correctamente.\n¿Desea descargar el PDF?", parent=modal):
                    from tkinter import filedialog
                    filename = filedialog.asksaveasfilename(
                        defaultextension=".pdf",
                        filetypes=[("PDF Files", "*.pdf")],
                        title="Guardar Receta",
                        parent=modal
                    )
                    if filename:
                        paciente = next((p for p in self.pacientes if p.id_paciente == self.selected_paciente_id), None)
                        turno = next((t for t in self.turnos_actuales if t.id_turno == self.selected_turno_id), None)
                        medico = self.controller.medico_service.obtener_por_id(turno.id_medico)
                        
                        self.controller.generar_pdf_receta_data(receta, paciente, medico, filename, diagnostico)
                        messagebox.showinfo("Exito", "PDF guardado correctamente.", parent=modal)
                
                modal.destroy()
                self._cargar_turnos()
                self._limpiar_formulario()

            except Exception as e:
                messagebox.showerror("Error", str(e), parent=modal)

        ttk.Button(modal, text="Guardar y Generar PDF", command=_guardar_receta, style='TButton').pack(pady=10) 

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
