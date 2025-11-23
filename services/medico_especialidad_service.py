
from services.database import DatabaseConnection

class MedicoEspecialidadService:

    def __init__(self):
        self.db = DatabaseConnection()
        self.con = self.db.get_connection()
        self.cur = self.db.get_cursor()

    def asignar(self, id_medico, id_especialidad):
        self.cur.execute("""
            INSERT OR IGNORE INTO medico_especialidad (id_medico, id_especialidad)
            VALUES (?, ?)
        """, (id_medico, id_especialidad))
        self.con.commit()

    def obtener_por_medico(self, id_medico):
        self.cur.execute("""
            SELECT id_especialidad
            FROM medico_especialidad
            WHERE id_medico = ?
        """, (id_medico,))
        return [row[0] for row in self.cur.fetchall()]
    
    def obtener_especialidades_de_medico(self, id_medico):
        self.cur.execute("""
            SELECT e.nombre
            FROM medico_especialidad me
            JOIN especialidad e ON e.id_especialidad = me.id_especialidad
            WHERE me.id_medico = ?
        """, (id_medico,))
        return [row[0] for row in self.cur.fetchall()]
