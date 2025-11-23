from services.database import DatabaseConnection
from model.turno import Turno
from model.estado_turno import EstadoTurno


class TurnoService:

    def __init__(self):
        self.db = DatabaseConnection()
        self.con = self.db.get_connection()
        self.cur = self.db.get_cursor()

    def crear(self, turno: Turno):
        self.cur.execute(
            """
            INSERT INTO turno (id_paciente, id_medico, fecha, hora, id_estado, motivo)
            VALUES (?, ?, ?, ?, ?, ?)
            """,
            (
                turno.id_paciente,
                turno.id_medico,
                turno.fecha,
                turno.hora,
                turno.id_estado,
                turno.motivo,
            ),
        )
        self.con.commit()
        turno.id_turno = self.cur.lastrowid
        return turno

    def actualizar(self, turno: Turno):
        self.cur.execute(
            """
            UPDATE turno
            SET id_paciente = ?, id_medico = ?, fecha = ?, hora = ?, id_estado = ?, motivo = ?
            WHERE id_turno = ?
            """,
            (
                turno.id_paciente,
                turno.id_medico,
                turno.fecha,
                turno.hora,
                turno.id_estado,
                turno.motivo,
                turno.id_turno,
            ),
        )
        self.con.commit()
        return turno

    def eliminar(self, id_turno):
        self.cur.execute("DELETE FROM turno WHERE id_turno = ?", (id_turno,))
        self.con.commit()

    def obtener_todos(self):
        self.cur.execute(
            """
            SELECT
                t.id_turno,
                t.id_paciente,
                p.nombre,
                p.apellido,
                t.id_medico,
                m.nombre,
                m.apellido,
                t.fecha,
                t.hora,
                t.id_estado,
                e.nombre,
                t.motivo
            FROM turno t
            JOIN paciente p ON p.id_paciente = t.id_paciente
            JOIN medico m ON m.id_medico = t.id_medico
            JOIN estado_turno e ON e.id_estado = t.id_estado
            ORDER BY t.fecha, t.hora
            """
        )
        rows = self.cur.fetchall()

        turnos = []
        for row in rows:
            turno = Turno(
                id_paciente=row[1],
                id_medico=row[4],
                fecha=row[7],
                hora=row[8],
                id_estado=row[9],
                motivo=row[11],
                id_turno=row[0],
                paciente_nombre=f"{row[3]}, {row[2]}",
                medico_nombre=f"{row[6]}, {row[5]}",
                estado_nombre=row[10],
            )
            turnos.append(turno)
        return turnos

    def obtener_por_paciente(self, id_paciente):
        self.cur.execute(
            """
            SELECT
                t.id_turno,
                t.id_paciente,
                p.nombre,
                p.apellido,
                t.id_medico,
                m.nombre,
                m.apellido,
                t.fecha,
                t.hora,
                t.id_estado,
                e.nombre,
                t.motivo
            FROM turno t
            JOIN paciente p ON p.id_paciente = t.id_paciente
            JOIN medico m ON m.id_medico = t.id_medico
            JOIN estado_turno e ON e.id_estado = t.id_estado
            WHERE t.id_paciente = ?
            ORDER BY t.fecha DESC, t.hora DESC
            """,
            (id_paciente,),
        )
        rows = self.cur.fetchall()

        turnos = []
        for row in rows:
            turnos.append(
                Turno(
                    id_paciente=row[1],
                    id_medico=row[4],
                    fecha=row[7],
                    hora=row[8],
                    id_estado=row[9],
                    motivo=row[11],
                    id_turno=row[0],
                    paciente_nombre=f"{row[3]}, {row[2]}",
                    medico_nombre=f"{row[6]}, {row[5]}",
                    estado_nombre=row[10],
                )
            )
        return turnos

    def obtener_por_id(self, id_turno):
        self.cur.execute(
            """
            SELECT
                t.id_turno,
                t.id_paciente,
                p.nombre,
                p.apellido,
                t.id_medico,
                m.nombre,
                m.apellido,
                t.fecha,
                t.hora,
                t.id_estado,
                e.nombre,
                t.motivo
            FROM turno t
            JOIN paciente p ON p.id_paciente = t.id_paciente
            JOIN medico m ON m.id_medico = t.id_medico
            JOIN estado_turno e ON e.id_estado = t.id_estado
            WHERE t.id_turno = ?
            """,
            (id_turno,),
        )
        row = self.cur.fetchone()

        if not row:
            return None

        return Turno(
            id_paciente=row[1],
            id_medico=row[4],
            fecha=row[7],
            hora=row[8],
            id_estado=row[9],
            motivo=row[11],
            id_turno=row[0],
            paciente_nombre=f"{row[3]}, {row[2]}",
            medico_nombre=f"{row[6]}, {row[5]}",
            estado_nombre=row[10],
        )

    def obtener_estados(self):
        self.cur.execute(
            "SELECT id_estado, nombre FROM estado_turno ORDER BY id_estado"
        )
        rows = self.cur.fetchall()

        estados = []
        for row in rows:
            estados.append(EstadoTurno(nombre=row[1], id_estado=row[0]))
        return estados

    def existe_conflicto(self, id_medico, fecha, hora, excluir_id=None):
        query = (
            "SELECT 1 FROM turno WHERE id_medico = ? AND fecha = ? AND hora = ?"
        )
        params = [id_medico, fecha, hora]

        if excluir_id is not None:
            query += " AND id_turno <> ?"
            params.append(excluir_id)

        self.cur.execute(query, tuple(params))
        return self.cur.fetchone() is not None
