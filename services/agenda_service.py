from services.database import DatabaseConnection
from model.agenda import Agenda

class AgendaService:

    def __init__(self):
        self.db = DatabaseConnection()
        self.con = self.db.get_connection()
        self.cur = self.db.get_cursor()

    # Crear agenda
    def crear(self, agenda: Agenda):
        self.cur.execute("""
            INSERT INTO agenda (id_medico, dia_semana, hora_desde, hora_hasta, duracion_turno_min)
            VALUES (?, ?, ?, ?, ?)
        """, (agenda.id_medico, agenda.dia_semana, agenda.hora_desde, agenda.hora_hasta, agenda.duracion_turno_min))
        self.con.commit()
        agenda.id_agenda = self.cur.lastrowid
        return agenda

    # Obtener agendas por médico
    def obtener_por_medico(self, id_medico):
        self.cur.execute("""
            SELECT id_agenda, id_medico, dia_semana, hora_desde, hora_hasta, duracion_turno_min
            FROM agenda
            WHERE id_medico = ?
            ORDER BY dia_semana, hora_desde
        """, (id_medico,))
        rows = self.cur.fetchall()

        agendas = []
        for r in rows:
            agendas.append(Agenda(
                id_agenda=r[0],
                id_medico=r[1],
                dia_semana=r[2],
                hora_desde=r[3],
                hora_hasta=r[4],
                duracion_turno_min=r[5]
            ))
        return agendas
    
    # Eliminar agenda
    def eliminar(self, id_agenda):
        self.cur.execute("DELETE FROM agenda WHERE id_agenda = ?", (id_agenda,))
        self.con.commit()

    # Verificar solapamiento de horarios
    def verificar_solapamiento(self, id_medico, dia_semana, hora_desde, hora_hasta):
        self.cur.execute("""
            SELECT id_agenda 
            FROM agenda
            WHERE id_medico = ? 
            AND dia_semana = ?
            AND (hora_desde < ? AND hora_hasta > ?)
        """, (id_medico, dia_semana, hora_hasta, hora_desde))
        
        row = self.cur.fetchone()
        return row is not None
    
    def obtener_por_medico_y_dia(self, id_medico, dia_semana):
        self.cur.execute("""
            SELECT id_agenda, id_medico, dia_semana, hora_desde, hora_hasta, duracion_turno_min
            FROM agenda
            WHERE id_medico = ? AND dia_semana = ?
        """, (id_medico, dia_semana))
        row = self.cur.fetchone()

        if row:
            return Agenda(
                id_agenda=row[0],
                id_medico=row[1],
                dia_semana=row[2],
                hora_desde=row[3],
                hora_hasta=row[4],
                duracion_turno_min=row[5]
            )
        return None
    
    def actualizar(self, agenda: Agenda):
        self.cur.execute("""
            UPDATE agenda
            SET dia_semana = ?, hora_desde = ?, hora_hasta = ?, duracion_turno_min = ?
            WHERE id_agenda = ?
        """, (agenda.dia_semana, agenda.hora_desde, agenda.hora_hasta, agenda.duracion_turno_min, agenda.id_agenda))
        self.con.commit()
        return agenda

    def verificar_solapamiento_actualizacion(self, id_agenda, id_medico, dia_semana, hora_desde, hora_hasta):
        self.cur.execute("""
            SELECT id_agenda 
            FROM agenda
            WHERE id_medico = ? 
            AND dia_semana = ?
            AND id_agenda != ?
            AND (hora_desde < ? AND hora_hasta > ?)
        """, (id_medico, dia_semana, id_agenda, hora_hasta, hora_desde))
        
        row = self.cur.fetchone()
        return row is not None