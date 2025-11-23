from services.database import DatabaseConnection
from model.historia_clinica import HistoriaClinica


class HistoriaClinicaService:

    def __init__(self):
        self.db = DatabaseConnection()
        self.con = self.db.get_connection()
        self.cur = self.db.get_cursor()

    def crear(self, historia: HistoriaClinica):
        self.cur.execute(
            """
            INSERT INTO historia_clinica (id_paciente, fecha, resumen, id_atencion)
            VALUES (?, ?, ?, ?)
            """,
            (
                historia.id_paciente,
                historia.fecha,
                historia.resumen,
                historia.id_atencion,
            ),
        )
        self.con.commit()
        historia.id_historia = self.cur.lastrowid
        return historia

    def actualizar(self, historia: HistoriaClinica):
        self.cur.execute(
            """
            UPDATE historia_clinica
            SET fecha = ?, resumen = ?, id_atencion = ?
            WHERE id_historia = ?
            """,
            (
                historia.fecha,
                historia.resumen,
                historia.id_atencion,
                historia.id_historia,
            ),
        )
        self.con.commit()
        return historia

    def eliminar(self, id_historia):
        self.cur.execute("DELETE FROM historia_clinica WHERE id_historia = ?", (id_historia,))
        self.con.commit()

    def obtener_por_id(self, id_historia):
        self.cur.execute(
            """
            SELECT id_historia, id_paciente, fecha, resumen, id_atencion
            FROM historia_clinica
            WHERE id_historia = ?
            """,
            (id_historia,),
        )
        row = self.cur.fetchone()
        if not row:
            return None

        return HistoriaClinica(
            id_paciente=row[1],
            fecha=row[2],
            resumen=row[3],
            id_atencion=row[4],
            id_historia=row[0],
        )

    def obtener_por_atencion(self, id_atencion):
        self.cur.execute(
            """
            SELECT id_historia, id_paciente, fecha, resumen, id_atencion
            FROM historia_clinica
            WHERE id_atencion = ?
            """,
            (id_atencion,),
        )
        row = self.cur.fetchone()
        if not row:
            return None

        return HistoriaClinica(
            id_paciente=row[1],
            fecha=row[2],
            resumen=row[3],
            id_atencion=row[4],
            id_historia=row[0],
        )

    def listar_por_paciente(self, id_paciente):
        self.cur.execute(
            """
            SELECT
                h.id_historia,
                h.id_paciente,
                h.fecha,
                h.resumen,
                h.id_atencion,
                a.diagnostico,
                a.procedimiento,
                a.indicaciones,
                t.fecha,
                t.hora,
                m.nombre,
                m.apellido,
                p.nombre,
                p.apellido
            FROM historia_clinica h
            LEFT JOIN atencion a ON a.id_atencion = h.id_atencion
            LEFT JOIN turno t ON t.id_turno = a.id_turno
            LEFT JOIN medico m ON m.id_medico = t.id_medico
            JOIN paciente p ON p.id_paciente = h.id_paciente
            WHERE h.id_paciente = ?
            ORDER BY h.fecha DESC, t.fecha DESC, t.hora DESC
            """,
            (id_paciente,),
        )

        rows = self.cur.fetchall()
        historias = []
        for row in rows:
            historias.append(
                HistoriaClinica(
                    id_paciente=row[1],
                    fecha=row[2],
                    resumen=row[3],
                    id_atencion=row[4],
                    id_historia=row[0],
                    diagnostico=row[5],
                    procedimiento=row[6],
                    indicaciones=row[7],
                    turno_fecha=row[8],
                    turno_hora=row[9],
                    medico_nombre=(
                        f"{row[11]}, {row[10]}" if row[10] and row[11] else None
                    ),
                    paciente_nombre=f"{row[13]}, {row[12]}",
                )
            )
        return historias
