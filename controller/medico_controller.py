
from services.medico_service import MedicoService
from model.medico import Medico

class MedicoController:

    def __init__(self):
        self.service = MedicoService()

    # Crear
    def crear_medico(self, datos: dict):
        if not datos.get("dni") or len(datos["dni"]) < 7:
            raise ValueError("El DNI es inválido.")

        if not datos.get("nombre"):
            raise ValueError("El nombre no puede estar vacío.")

        if not datos.get("apellido"):
            raise ValueError("El apellido no puede estar vacío.")

        if not datos.get("matricula"):
            raise ValueError("La matrícula no puede estar vacía.")

        # Validar DNI único
        if self.service.obtener_por_dni(datos["dni"]):
            raise ValueError("Ya existe un médico con ese DNI.")

        # Validar matrícula única
        if self.service.obtener_por_matricula(datos["matricula"]):
            raise ValueError("Ya existe un médico con esa matrícula.")

        medico = Medico(
            dni=datos["dni"],
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            matricula=datos["matricula"],
            telefono=datos.get("telefono")
        )

        return self.service.crear(medico)

    # Actualizar
    def actualizar_medico(self, id_medico, datos: dict):
        medico = self.service.obtener_por_id(id_medico)

        if not medico:
            raise ValueError("El médico no existe.")

        if not datos.get("dni") or len(datos["dni"]) < 7:
            raise ValueError("El DNI es inválido.")

        if not datos.get("nombre"):
            raise ValueError("El nombre no puede estar vacío.")

        if not datos.get("apellido"):
            raise ValueError("El apellido no puede estar vacío.")

        if not datos.get("matricula"):
            raise ValueError("La matrícula no puede estar vacía.")

        # DNI duplicado
        otro = self.service.obtener_por_dni(datos["dni"])
        if otro and otro.id_medico != id_medico:
            raise ValueError("Otro médico ya tiene ese DNI.")

        # Matrícula duplicada
        otro = self.service.obtener_por_matricula(datos["matricula"])
        if otro and otro.id_medico != id_medico:
            raise ValueError("Otro médico ya tiene esa matrícula.")

        medico.dni = datos["dni"]
        medico.nombre = datos["nombre"]
        medico.apellido = datos["apellido"]
        medico.matricula = datos["matricula"]
        medico.telefono = datos.get("telefono")

        self.service.actualizar(medico)
        return medico

    # Eliminar
    def eliminar_medico(self, id_medico):
        if not self.service.obtener_por_id(id_medico):
            raise ValueError("El médico no existe.")
        self.service.eliminar(id_medico)

    # Listar
    def listar_medicos(self):
        return self.service.obtener_todos()
