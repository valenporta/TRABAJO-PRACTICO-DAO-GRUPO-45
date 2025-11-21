import sqlite3

class DatabaseConnection:
    _instance = None
    _db_path = "database.db"

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(DatabaseConnection, cls).__new__(cls)
            cls._instance.connection = sqlite3.connect(cls._db_path)
            cls._instance.cursor = cls._instance.connection.cursor()
            cls._instance.connection.execute("PRAGMA foreign_keys = ON;")
        return cls._instance

    def get_connection(self):
        return self.connection

    def get_cursor(self):
        return self.cursor

    def initialize_database(self):
        """Crea todas las tablas si no existen."""
        con = self.connection
        cur = self.cursor

        # ESPECIALIDAD
        cur.execute("""
        CREATE TABLE IF NOT EXISTS especialidad (
            id_especialidad INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL UNIQUE
        );
        """)

        # MEDICO
        cur.execute("""
        CREATE TABLE IF NOT EXISTS medico (
            id_medico INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            matricula TEXT NOT NULL UNIQUE,
            telefono TEXT
        );
        """)

        # MEDICO-ESPECIALIDAD (N-N)
        cur.execute("""
        CREATE TABLE IF NOT EXISTS medico_especialidad (
            id_medico INTEGER NOT NULL,
            id_especialidad INTEGER NOT NULL,
            PRIMARY KEY (id_medico, id_especialidad),
            FOREIGN KEY (id_medico) REFERENCES medico(id_medico) ON DELETE CASCADE,
            FOREIGN KEY (id_especialidad) REFERENCES especialidad(id_especialidad) ON DELETE CASCADE
        );
        """)

        # PACIENTE
        cur.execute("""
        CREATE TABLE IF NOT EXISTS paciente (
            id_paciente INTEGER PRIMARY KEY AUTOINCREMENT,
            dni TEXT NOT NULL UNIQUE,
            nombre TEXT NOT NULL,
            apellido TEXT NOT NULL,
            telefono TEXT,
            email TEXT,
            fecha_nac TEXT
        );
        """)

        # AGENDA
        cur.execute("""
        CREATE TABLE IF NOT EXISTS agenda (
            id_agenda INTEGER PRIMARY KEY AUTOINCREMENT,
            id_medico INTEGER NOT NULL,
            dia_semana INTEGER NOT NULL,
            hora_desde TEXT NOT NULL,
            hora_hasta TEXT NOT NULL,
            duracion_turno_min INTEGER NOT NULL,
            FOREIGN KEY (id_medico) REFERENCES medico(id_medico)
        );
        """)

        # ESTADOS DE TURNO
        cur.execute("""
        CREATE TABLE IF NOT EXISTS estado_turno (
            id_estado INTEGER PRIMARY KEY,
            nombre TEXT NOT NULL UNIQUE
        );
        """)

        # Insertar estados por defecto
        cur.executemany(
            "INSERT OR IGNORE INTO estado_turno (id_estado, nombre) VALUES (?, ?)",
            [
                (1, "Pendiente"),
                (2, "Atendido"),
                (3, "Cancelado"),
                (4, "Ausente")
            ]
        )

        # TURNO
        cur.execute("""
        CREATE TABLE IF NOT EXISTS turno (
            id_turno INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER NOT NULL,
            id_medico INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            hora TEXT NOT NULL,
            id_estado INTEGER NOT NULL DEFAULT 1,
            motivo TEXT,
            FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente),
            FOREIGN KEY (id_medico) REFERENCES medico(id_medico),
            FOREIGN KEY (id_estado) REFERENCES estado_turno(id_estado),
            UNIQUE(id_medico, fecha, hora)
        );
        """)

        # ATENCION
        cur.execute("""
        CREATE TABLE IF NOT EXISTS atencion (
            id_atencion INTEGER PRIMARY KEY AUTOINCREMENT,
            id_turno INTEGER NOT NULL UNIQUE,
            diagnostico TEXT,
            procedimiento TEXT,
            indicaciones TEXT,
            FOREIGN KEY (id_turno) REFERENCES turno(id_turno)
        );
        """)

        # RECETA
        cur.execute("""
        CREATE TABLE IF NOT EXISTS receta (
            id_receta INTEGER PRIMARY KEY AUTOINCREMENT,
            id_atencion INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            detalle TEXT NOT NULL,
            FOREIGN KEY (id_atencion) REFERENCES atencion(id_atencion)
        );
        """)

        # HISTORIA CLINICA
        cur.execute("""
        CREATE TABLE IF NOT EXISTS historia_clinica (
            id_historia INTEGER PRIMARY KEY AUTOINCREMENT,
            id_paciente INTEGER NOT NULL,
            fecha TEXT NOT NULL,
            resumen TEXT,
            id_atencion INTEGER,
            FOREIGN KEY (id_paciente) REFERENCES paciente(id_paciente),
            FOREIGN KEY (id_atencion) REFERENCES atencion(id_atencion)
        );
        """)

        con.commit()
        print("Base de datos inicializada correctamente.")
