
from services.especialidad_service import EspecialidadService
from model.especialidad import Especialidad

class EspecialidadController:

    def __init__(self):
        self.service = EspecialidadService()

    # Crear
    def crear_especialidad(self, datos: dict):
        if not datos.get("nombre"):
            raise ValueError("El nombre de la especialidad no puede estar vacío.")

        if self.service.obtener_por_nombre(datos["nombre"]):
            raise ValueError("Ya existe una especialidad con ese nombre.")

        esp = Especialidad(nombre=datos["nombre"])
        return self.service.crear(esp)

    # Actualizar
    def actualizar_especialidad(self, id_especialidad, datos: dict):
        esp = self.service.obtener_por_id(id_especialidad)
        if not esp:
            raise ValueError("La especialidad no existe.")

        if not datos.get("nombre"):
            raise ValueError("El nombre no puede estar vacío.")

        otra = self.service.obtener_por_nombre(datos["nombre"])
        if otra and otra.id_especialidad != id_especialidad:
            raise ValueError("Ya existe otra especialidad con ese nombre.")

        esp.nombre = datos["nombre"]
        self.service.actualizar(esp)
        return esp

    # Eliminar
    def eliminar_especialidad(self, id_especialidad):
        esp = self.service.obtener_por_id(id_especialidad)
        if not esp:
            raise ValueError("La especialidad no existe.")
        self.service.eliminar(id_especialidad)

    # Listar
    def listar_especialidades(self):
        return self.service.obtener_todas()
