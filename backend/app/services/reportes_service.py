from typing import List, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import text

# Reporte: listado de turnos por médico en un período
def turnos_por_medico(db: Session, medico_id: int, desde: str, hasta: str):
    sql = text("""        SELECT t.id, t.fecha_hora, t.estado, p.apellido||', '||p.nombre AS paciente
    FROM turnos t
    JOIN pacientes p ON p.id = t.paciente_id
    WHERE t.medico_id = :mid AND t.fecha_hora BETWEEN :desde AND :hasta
    ORDER BY t.fecha_hora
    """)
    return [dict(r) for r in db.execute(sql, {"mid": medico_id, "desde": desde, "hasta": hasta}).mappings().all()]

# Reporte: cantidad de turnos por especialidad
# Usa especialidad_id del turno si existe; si no, agrupa como 'Sin especialidad'
def turnos_por_especialidad(db: Session, desde: str, hasta: str):
    sql = text("""        SELECT COALESCE(e.nombre, 'Sin especialidad') AS especialidad, COUNT(*) AS cantidad
    FROM turnos t
    LEFT JOIN especialidades e ON e.id = t.especialidad_id
    WHERE t.fecha_hora BETWEEN :desde AND :hasta
    GROUP BY COALESCE(e.nombre, 'Sin especialidad')
    ORDER BY cantidad DESC
    """)
    return [dict(r) for r in db.execute(sql, {"desde": desde, "hasta": hasta}).mappings().all()]

# Reporte: pacientes atendidos en rango
def pacientes_atendidos(db: Session, desde: str, hasta: str):
    sql = text("""        SELECT DISTINCT p.id, p.apellido||', '||p.nombre AS paciente
    FROM turnos t
    JOIN pacientes p ON p.id = t.paciente_id
    WHERE t.estado = 'atendido' AND t.fecha_hora BETWEEN :desde AND :hasta
    ORDER BY paciente
    """)
    return [dict(r) for r in db.execute(sql, {"desde": desde, "hasta": hasta}).mappings().all()]

# Reporte: asistencia vs inasistencias
def asistencia_vs_inasistencias(db: Session, desde: str, hasta: str):
    sql = text("""        SELECT t.estado, COUNT(*) cantidad
    FROM turnos t
    WHERE t.fecha_hora BETWEEN :desde AND :hasta
    GROUP BY t.estado
    """)
    rows = [dict(r) for r in db.execute(sql, {"desde": desde, "hasta": hasta}).mappings().all()]
    mapa = {r['estado']: r['cantidad'] for r in rows}
    return {
        "atendidos": mapa.get('atendido', 0),
        "ausentes": mapa.get('ausente', 0),
        "cancelados": mapa.get('cancelado', 0),
        "confirmados": mapa.get('confirmado', 0),
        "reservados": mapa.get('reservado', 0),
    }
