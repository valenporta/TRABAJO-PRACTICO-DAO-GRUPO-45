
from services.database import DatabaseConnection
from model.especialidad import Especialidad

class EspecialidadService:

    def __init__(self):
        self.db = DatabaseConnection()
        self.con = self.db.get_connection()
        self.cur = self.db.get_cursor()

    # Crear especialidad
    def crear(self, especialidad: Especialidad):
        self.cur.execute("""
            INSERT INTO especialidad (nombre)
            VALUES (?)
        """, (especialidad.nombre,))
        self.con.commit()
        especialidad.id_especialidad = self.cur.lastrowid
        return especialidad

    # Listar todas
    def obtener_todas(self):
        self.cur.execute("""
            SELECT id_especialidad, nombre
            FROM especialidad
            ORDER BY nombre
        """)
        rows = self.cur.fetchall()

        especialidades = []
        for r in rows:
            especialidades.append(Especialidad(
                nombre=r[1],
                id_especialidad=r[0]
            ))
        return especialidades

    # Obtener por ID
    def obtener_por_id(self, id_especialidad):
        self.cur.execute("""
            SELECT id_especialidad, nombre
            FROM especialidad
            WHERE id_especialidad = ?
        """, (id_especialidad,))
        r = self.cur.fetchone()
        if not r:
            return None
        return Especialidad(nombre=r[1], id_especialidad=r[0])

    # Obtener por nombre
    def obtener_por_nombre(self, nombre):
        self.cur.execute("""
            SELECT id_especialidad, nombre
            FROM especialidad
            WHERE nombre = ?
        """, (nombre,))
        r = self.cur.fetchone()
        if not r:
            return None
        return Especialidad(nombre=r[1], id_especialidad=r[0])

    # Actualizar
    def actualizar(self, especialidad: Especialidad):
        self.cur.execute("""
            UPDATE especialidad
            SET nombre = ?
            WHERE id_especialidad = ?
        """, (especialidad.nombre, especialidad.id_especialidad))
        self.con.commit()

    # Eliminar
    def eliminar(self, id_especialidad):
        self.cur.execute("DELETE FROM especialidad WHERE id_especialidad = ?", (id_especialidad,))
        self.con.commit()
