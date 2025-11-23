from services.database import DatabaseConnection
from model.atencion import Atencion


class AtencionService:

    def __init__(self):
        self.db = DatabaseConnection()
        self.con = self.db.get_connection()
        self.cur = self.db.get_cursor()

    def crear(self, atencion: Atencion):
        self.cur.execute(
            """
            INSERT INTO atencion (id_turno, diagnostico, procedimiento, indicaciones)
            VALUES (?, ?, ?, ?)
            """,
            (
                atencion.id_turno,
                atencion.diagnostico,
                atencion.procedimiento,
                atencion.indicaciones,
            ),
        )
        self.con.commit()
        atencion.id_atencion = self.cur.lastrowid
        return atencion

    def actualizar(self, atencion: Atencion):
        self.cur.execute(
            """
            UPDATE atencion
            SET diagnostico = ?, procedimiento = ?, indicaciones = ?
            WHERE id_atencion = ?
            """,
            (
                atencion.diagnostico,
                atencion.procedimiento,
                atencion.indicaciones,
                atencion.id_atencion,
            ),
        )
        self.con.commit()
        return atencion

    def eliminar(self, id_atencion):
        self.cur.execute("DELETE FROM atencion WHERE id_atencion = ?", (id_atencion,))
        self.con.commit()

    def obtener_por_turno(self, id_turno):
        self.cur.execute(
            """
            SELECT id_atencion, id_turno, diagnostico, procedimiento, indicaciones
            FROM atencion
            WHERE id_turno = ?
            """,
            (id_turno,),
        )
        row = self.cur.fetchone()
        if not row:
            return None

        return Atencion(
            id_turno=row[1],
            diagnostico=row[2],
            procedimiento=row[3],
            indicaciones=row[4],
            id_atencion=row[0],
        )

    def listar_por_paciente(self, id_paciente):
        self.cur.execute(
            """
            SELECT
                a.id_atencion,
                a.id_turno,
                a.diagnostico,
                a.procedimiento,
                a.indicaciones,
                t.fecha,
                t.hora,
                m.nombre,
                m.apellido,
                p.nombre,
                p.apellido
            FROM atencion a
            JOIN turno t ON t.id_turno = a.id_turno
            JOIN medico m ON m.id_medico = t.id_medico
            JOIN paciente p ON p.id_paciente = t.id_paciente
            WHERE p.id_paciente = ?
            ORDER BY t.fecha DESC, t.hora DESC
            """,
            (id_paciente,),
        )

        rows = self.cur.fetchall()
        atenciones = []
        for row in rows:
            atenciones.append(
                Atencion(
                    id_turno=row[1],
                    diagnostico=row[2],
                    procedimiento=row[3],
                    indicaciones=row[4],
                    id_atencion=row[0],
                    turno_fecha=row[5],
                    turno_hora=row[6],
                    medico_nombre=f"{row[8]}, {row[7]}",
                    paciente_nombre=f"{row[10]}, {row[9]}",
                )
            )
        return atenciones
