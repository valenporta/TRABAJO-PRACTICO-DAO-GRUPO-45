
from services.database import DatabaseConnection
from model.paciente import Paciente

class PacienteService:

    def __init__(self):
        self.db = DatabaseConnection()
        self.con = self.db.get_connection()
        self.cur = self.db.get_cursor()

    # ---------------------------------------------------
    # Crear paciente
    # ---------------------------------------------------
    def crear(self, paciente: Paciente):
        self.cur.execute("""
            INSERT INTO paciente (dni, nombre, apellido, telefono, email, fecha_nac)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (
            paciente.dni,
            paciente.nombre,
            paciente.apellido,
            paciente.telefono,
            paciente.email,
            paciente.fecha_nac
        ))
        self.con.commit()
        paciente.id_paciente = self.cur.lastrowid
        return paciente

    # ---------------------------------------------------
    # Listar todos los pacientes
    # ---------------------------------------------------
    def obtener_todos(self):
        self.cur.execute("""
            SELECT id_paciente, dni, nombre, apellido, telefono, email, fecha_nac
            FROM paciente
            ORDER BY apellido, nombre
        """)
        rows = self.cur.fetchall()

        pacientes = []
        for r in rows:
            pacientes.append(Paciente(
                dni=r[1],
                nombre=r[2],
                apellido=r[3],
                telefono=r[4],
                email=r[5],
                fecha_nac=r[6],
                id_paciente=r[0]
            ))
        return pacientes

    # ---------------------------------------------------
    # Obtener por ID
    # ---------------------------------------------------
    def obtener_por_id(self, id_paciente):
        self.cur.execute("""
            SELECT id_paciente, dni, nombre, apellido, telefono, email, fecha_nac
            FROM paciente
            WHERE id_paciente = ?
        """, (id_paciente,))
        r = self.cur.fetchone()

        if r is None:
            return None
        
        return Paciente(
            dni=r[1],
            nombre=r[2],
            apellido=r[3],
            telefono=r[4],
            email=r[5],
            fecha_nac=r[6],
            id_paciente=r[0]
        )

    # ---------------------------------------------------
    # Buscar por DNI
    # ---------------------------------------------------
    def obtener_por_dni(self, dni):
        self.cur.execute("""
            SELECT id_paciente, dni, nombre, apellido, telefono, email, fecha_nac
            FROM paciente
            WHERE dni = ?
        """, (dni,))
        r = self.cur.fetchone()

        if r is None:
            return None
        
        return Paciente(
            dni=r[1],
            nombre=r[2],
            apellido=r[3],
            telefono=r[4],
            email=r[5],
            fecha_nac=r[6],
            id_paciente=r[0]
        )

    # ---------------------------------------------------
    # Actualizar paciente
    # ---------------------------------------------------
    def actualizar(self, paciente: Paciente):
        self.cur.execute("""
            UPDATE paciente
            SET dni = ?, nombre = ?, apellido = ?, telefono = ?, email = ?, fecha_nac = ?
            WHERE id_paciente = ?
        """, (
            paciente.dni,
            paciente.nombre,
            paciente.apellido,
            paciente.telefono,
            paciente.email,
            paciente.fecha_nac,
            paciente.id_paciente
        ))
        self.con.commit()

    # ---------------------------------------------------
    # Eliminar paciente
    # ---------------------------------------------------
    def eliminar(self, id_paciente):
        self.cur.execute("DELETE FROM paciente WHERE id_paciente = ?", (id_paciente,))
        self.con.commit()
