from services.database import DatabaseConnection
from model.receta import Receta

class RecetaService:
    def __init__(self):
        self.db = DatabaseConnection()
        self.con = self.db.get_connection()
        self.cur = self.db.get_cursor()

    def crear(self, receta: Receta):
        self.cur.execute(
            """
            INSERT INTO receta (id_atencion, fecha, detalle)
            VALUES (?, ?, ?)
            """,
            (receta.id_atencion, receta.fecha, receta.detalle),
        )
        self.con.commit()
        receta.id_receta = self.cur.lastrowid
        return receta

    def obtener_por_atencion(self, id_atencion):
        self.cur.execute(
            """
            SELECT id_receta, id_atencion, fecha, detalle
            FROM receta
            WHERE id_atencion = ?
            """,
            (id_atencion,),
        )
        row = self.cur.fetchone()
        if not row:
            return None
        
        return Receta(
            id_receta=row[0],
            id_atencion=row[1],
            fecha=row[2],
            detalle=row[3]
        )
