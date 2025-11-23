# Archivo: services/data_seeder.py

from .database import DatabaseConnection
from datetime import datetime, timedelta

class DataSeeder:
    
    def __init__(self):
        self.db = DatabaseConnection()
        self.cursor = self.db.get_cursor()
        self.conn = self.db.get_connection()
        self.ids = {} # Diccionario para guardar IDs generados para usar en otras tablas
        
    def _seed_especialidades(self):
        # ... (código que ya tienes para especialidades)
        datos_especialidades = [("Cardiología",), ("Dermatología",), ("Pediatría",)]
        sql_insert = "INSERT OR IGNORE INTO especialidad (nombre) VALUES (?)"
        
        self.cursor.executemany(sql_insert, datos_especialidades)
        self.conn.commit()
        
        # Guardamos los IDs de las especialidades para usarlos después
        self.cursor.execute("SELECT id_especialidad, nombre FROM especialidad")
        self.ids['especialidades'] = {row[1]: row[0] for row in self.cursor.fetchall()}
        print(f"[{__class__.__name__}] Especialidades sembradas: {len(self.ids['especialidades'])}")


    def _seed_medicos(self):
        # Campos: dni, nombre, apellido, matricula, telefono
        datos_medicos = [
            ("12345678", "Laura", "Giménez", "M1001", "1123456780"),
            ("87654321", "Roberto", "Vázquez", "M1002", "1123456781")
        ]
        sql_insert = "INSERT OR IGNORE INTO medico (dni, nombre, apellido, matricula, telefono) VALUES (?, ?, ?, ?, ?)"
        
        self.cursor.executemany(sql_insert, datos_medicos)
        self.conn.commit()
        
        # Guardamos los IDs de los médicos
        self.cursor.execute("SELECT id_medico, matricula FROM medico")
        self.ids['medicos'] = {row[1]: row[0] for row in self.cursor.fetchall()}
        print(f"[{__class__.__name__}] Médicos sembrados: {len(self.ids['medicos'])}")


    def _seed_agenda(self):
        # Asegúrate de que tienes IDs de médicos cargados (ej. 'M1001', 'M1002')
        if 'medicos' not in self.ids or not self.ids['medicos']:
            print("[DataSeeder] Advertencia: No hay médicos para crear agendas.")
            return

        # Usamos el ID del Dr. Laura Giménez (M1001) para un ejemplo
        id_medico_laura = self.ids['medicos']['M1001'] 
        id_medico_roberto = self.ids['medicos']['M1002'] 

        # Campos: id_medico, dia_semana, hora_desde, hora_hasta, duracion_turno_min
        # LUNES (1) y MIÉRCOLES (3) para Laura, de 9:00 a 13:00, turnos de 20 min
        # JUEVES (4) para Roberto, de 14:00 a 18:00, turnos de 30 min
        datos_agenda = [
            (id_medico_laura, 1, "09:00", "13:00", 20),
            (id_medico_laura, 3, "09:00", "13:00", 20),
            (id_medico_roberto, 4, "14:00", "18:00", 30),
        ]

        sql_insert = """
            INSERT INTO agenda (id_medico, dia_semana, hora_desde, hora_hasta, duracion_turno_min) 
            VALUES (?, ?, ?, ?, ?)
        """
        
        try:
            self.cursor.executemany(sql_insert, datos_agenda)
            self.conn.commit()
            print(f"[{__class__.__name__}] Agendas de prueba sembradas: {self.cursor.rowcount}")
        except Exception as e:
            print(f"Error al sembrar agendas: {e}")

    def _seed_medico_especialidad(self):
        # Usamos los IDs que guardamos en los pasos anteriores
        
        # Laura Giménez (M1001) es Pediatra
        id_medico_laura = self.ids['medicos']['M1001']
        id_especialidad_pediatria = self.ids['especialidades']['Pediatría']
        
        # Roberto Vázquez (M1002) es Cardiólogo
        id_medico_roberto = self.ids['medicos']['M1002']
        id_especialidad_cardiologia = self.ids['especialidades']['Cardiología']

        datos_relacion = [
            (id_medico_laura, id_especialidad_pediatria),
            (id_medico_roberto, id_especialidad_cardiologia),
        ]
        
        sql_insert = "INSERT OR IGNORE INTO medico_especialidad (id_medico, id_especialidad) VALUES (?, ?)"
        self.cursor.executemany(sql_insert, datos_relacion)
        self.conn.commit()
        print(f"[{__class__.__name__}] Relaciones Médico-Especialidad sembradas: {self.cursor.rowcount}")

    # ... Y así sucesivamente para las otras tablas
    
    def _seed_pacientes(self):
        # Campos: dni, nombre, apellido, telefono, email, fecha_nac
        datos_pacientes = [
            ("11111111", "Martina", "Di Pasquo", "1130001000", "m.dp@mail.com", "1995-05-15"),
            ("22222222", "Javier", "Fernández", "1130001001", "j.f@mail.com", "1980-12-01"),
            ("33333333", "Limon", "Manzana", "1130001002", "", ""),
            ("44444444", "Pera", "Manzana", "1130001004", "", ""),
            ("55555555", "Eugenia", "Sandia", "1130001006", "", "")
        ]
        sql_insert = "INSERT OR IGNORE INTO paciente (dni, nombre, apellido, telefono, email, fecha_nac) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.executemany(sql_insert, datos_pacientes)
        self.conn.commit()
        
        self.cursor.execute("SELECT id_paciente, dni FROM paciente")
        self.ids['pacientes'] = {row[1]: row[0] for row in self.cursor.fetchall()}
        print(f"[{__class__.__name__}] Pacientes sembrados: {len(self.ids['pacientes'])}")


    def _seed_agenda_y_turnos(self):
        # Configuramos una agenda para el Dr. Vázquez (Cardiología)
        id_medico_roberto = self.ids['medicos']['M1002']
        
        # AGENDA: Lunes (día 1), de 8:00 a 12:00, turnos de 30 min
        # Campos: id_medico, dia_semana, hora_desde, hora_hasta, duracion_turno_min
        datos_agenda = [(id_medico_roberto, 1, "08:00", "12:00", 30)]
        sql_agenda = "INSERT OR IGNORE INTO agenda (id_medico, dia_semana, hora_desde, hora_hasta, duracion_turno_min) VALUES (?, ?, ?, ?, ?)"
        self.cursor.executemany(sql_agenda, datos_agenda)
        self.conn.commit()
        print(f"[{__class__.__name__}] Agendas sembradas: {self.cursor.rowcount}")

        
        # TURNOS: Creamos un turno para el paciente Martina el próximo Lunes
        id_paciente_martina = self.ids['pacientes']['11111111']
        
        # Encontramos la fecha del próximo Lunes
        hoy = datetime.now()
        proximo_lunes = hoy + timedelta(days=(7 - hoy.weekday() + 0) % 7) # Lunes es 0, sumamos 0
        fecha_turno = proximo_lunes.strftime('%Y-%m-%d')
        
        # Campos: id_paciente, id_medico, fecha, hora, id_estado, motivo
        datos_turnos = [
            (id_paciente_martina, id_medico_roberto, fecha_turno, "08:30", 1, "Control anual"), # Pendiente
        ]
        sql_turnos = "INSERT OR IGNORE INTO turno (id_paciente, id_medico, fecha, hora, id_estado, motivo) VALUES (?, ?, ?, ?, ?, ?)"
        self.cursor.executemany(sql_turnos, datos_turnos)
        self.conn.commit()
        print(f"[{__class__.__name__}] Turnos de prueba sembrados: {self.cursor.rowcount}")


    def run(self):
        """Ejecuta todos los métodos de inicialización en el orden correcto."""
        print("\n--- Iniciando Data Seeder ---")
        
        # Paso 1: Datos Maestros (sin dependencias)
        self._seed_especialidades()
        self._seed_medicos()
        self._seed_pacientes()
        
        # Paso 2: Datos de Relación (dependen de los Maestros)
        self._seed_medico_especialidad()
        self._seed_agenda()

        # Paso 3: Datos de Flujo (dependen de todo lo anterior)
        self._seed_agenda_y_turnos()
        # Nota: La inserción de ATENCION y RECETA es más compleja porque requiere
        # saber el ID del turno recién creado y sería mejor hacer una lógica
        # más detallada o simplemente usar la app para crear ese tipo de datos.

        print("--- Data Seeder finalizado ---\n")