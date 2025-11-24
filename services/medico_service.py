from services.database import DatabaseConnection
from model.medico import Medico

class MedicoService:

    def __init__(self):
        self.db = DatabaseConnection()
        self.con = self.db.get_connection()
        self.cur = self.db.get_cursor()

    # Crear médico
    def crear(self, medico: Medico):
        self.cur.execute("""
            INSERT INTO medico (dni, nombre, apellido, matricula, telefono)
            VALUES (?, ?, ?, ?, ?)
        """, (
            medico.dni,
            medico.nombre,
            medico.apellido,
            medico.matricula,
            medico.telefono
        ))
        self.con.commit()
        medico.id_medico = self.cur.lastrowid
        return medico

    # Obtener todos
    def obtener_todos(self):
        self.cur.execute("""
            SELECT id_medico, dni, nombre, apellido, matricula, telefono
            FROM medico
            ORDER BY apellido, nombre
        """)
        rows = self.cur.fetchall()

        medicos = []
        for r in rows:
            medicos.append(Medico(
                dni=r[1],
                nombre=r[2],
                apellido=r[3],
                matricula=r[4],
                telefono=r[5],
                id_medico=r[0]
            ))
        return medicos

    # Obtener por ID
    def obtener_por_id(self, id_medico):
        self.cur.execute("""
            SELECT id_medico, dni, nombre, apellido, matricula, telefono
            FROM medico
            WHERE id_medico = ?
        """, (id_medico,))
        r = self.cur.fetchone()

        if not r:
            return None

        return Medico(
            dni=r[1],
            nombre=r[2],
            apellido=r[3],
            matricula=r[4],
            telefono=r[5],
            id_medico=r[0]
        )

    # Buscar por DNI
    def obtener_por_dni(self, dni):
        self.cur.execute("""
            SELECT id_medico, dni, nombre, apellido, matricula, telefono
            FROM medico
            WHERE dni = ?
        """, (dni,))
        r = self.cur.fetchone()
        if not r:
            return None
        return Medico(r[1], r[2], r[3], r[4], r[5], id_medico=r[0])

    # Buscar por matrícula
    def obtener_por_matricula(self, matricula):
        self.cur.execute("""
            SELECT id_medico, dni, nombre, apellido, matricula, telefono
            FROM medico
            WHERE matricula = ?
        """, (matricula,))
        r = self.cur.fetchone()
        if not r:
            return None
        return Medico(r[1], r[2], r[3], r[4], r[5], id_medico=r[0])

    # ---------------------------------------------------
    # NUEVO MÉTODO: Validar DNI único (excluyendo ID)
    # ---------------------------------------------------
    def dni_existe_en_otro_medico(self, dni, id_medico_a_excluir):
        """
        Verifica si un DNI ya está registrado por OTRO médico, excluyendo al ID actual.
        """
        query = "SELECT id_medico FROM medico WHERE dni = ? AND id_medico != ?"
        
        self.cur.execute(query, (dni, id_medico_a_excluir))
        
        # Si fetchone() devuelve un resultado, SÍ existe otro médico con ese DNI.
        return self.cur.fetchone() is not None

    # ---------------------------------------------------
    # NUEVO MÉTODO: Validar Matrícula única (excluyendo ID)
    # ---------------------------------------------------
    def matricula_existe_en_otro_medico(self, matricula, id_medico_a_excluir):
        """
        Verifica si una Matrícula ya está registrada por OTRO médico, excluyendo al ID actual.
        """
        query = "SELECT id_medico FROM medico WHERE matricula = ? AND id_medico != ?"
        
        self.cur.execute(query, (matricula, id_medico_a_excluir))
        
        # Si fetchone() devuelve un resultado, SÍ existe otro médico con esa matrícula.
        return self.cur.fetchone() is not None


    # Actualizar
    def actualizar(self, medico: Medico):
        self.cur.execute("""
            UPDATE medico
            SET dni=?, nombre=?, apellido=?, matricula=?, telefono=?
            WHERE id_medico=?
        """, (
            medico.dni,
            medico.nombre,
            medico.apellido,
            medico.matricula,
            medico.telefono,
            medico.id_medico
        ))
        self.con.commit()

    # Eliminar
    def eliminar(self, id_medico):
        self.cur.execute("DELETE FROM medico WHERE id_medico = ?", (id_medico,))
        self.con.commit()