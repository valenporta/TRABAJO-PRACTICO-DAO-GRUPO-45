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
    # NUEVO MÉTODO: Validar DNI único (excluyendo ID)
    # ---------------------------------------------------
    def dni_existe_en_otro_paciente(self, dni, id_paciente_a_excluir=None):
        """
        Verifica si un DNI ya está registrado por OTRO paciente.
        ...
        """
        
        # Consulta base: busca un paciente con este DNI
        query = "SELECT id_paciente FROM paciente WHERE dni = ?"
        params = [dni]
        
        if id_paciente_a_excluir is not None:
            # Añadir la condición de exclusión para ACTUALIZACIÓN
            query += " AND id_paciente != ?"
            params.append(id_paciente_a_excluir)
            
        self.cur.execute(query, tuple(params))
        
        # Si fetchone() devuelve un resultado, SÍ existe otro paciente con ese DNI.
        return self.cur.fetchone() is not None

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

    def obtener_pacientes_atendidos_en_rango(self, fecha_inicio, fecha_fin):
        # Modificación: Agregamos "AND e.nombre = 'Atendido'" para filtrar
        query = """
            SELECT 
                t.fecha,
                t.hora,
                p.nombre,
                p.apellido,
                p.dni,
                m.apellido as medico,
                e.nombre as estado
            FROM turno t
            JOIN paciente p ON t.id_paciente = p.id_paciente
            JOIN medico m ON t.id_medico = m.id_medico
            JOIN estado_turno e ON t.id_estado = e.id_estado
            WHERE (t.fecha BETWEEN ? AND ?) 
            AND e.nombre = 'Atendido'
            ORDER BY t.fecha, p.apellido
        """
        self.cur.execute(query, (fecha_inicio, fecha_fin))
        return self.cur.fetchall()