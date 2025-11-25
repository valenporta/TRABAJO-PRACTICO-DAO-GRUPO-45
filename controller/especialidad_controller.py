import unicodedata
from services.especialidad_service import EspecialidadService
from model.especialidad import Especialidad

class EspecialidadController:

    def __init__(self):
        self.service = EspecialidadService()

    def _normalizar_texto(self, texto: str) -> str:

        if not texto:
            return ""
        
        texto_normalizado = unicodedata.normalize('NFD', texto)
        return ''.join(c for c in texto_normalizado if unicodedata.category(c) != 'Mn').lower().strip()

    # Crear
    def crear_especialidad(self, datos: dict):
        nombre_input = datos.get("nombre")
        if not nombre_input:
            raise ValueError("El nombre de la especialidad no puede estar vacío.")


        nombre_norm = self._normalizar_texto(nombre_input)
        todas = self.service.obtener_todas()

        for esp in todas:
            if self._normalizar_texto(esp.nombre) == nombre_norm:
                raise ValueError(f"Ya existe una especialidad con el nombre '{esp.nombre}' (similar a '{nombre_input}').")

        esp = Especialidad(nombre=nombre_input) 
        return self.service.crear(esp)

    # Actualizar
    def actualizar_especialidad(self, id_especialidad, datos: dict):
        esp_actual = self.service.obtener_por_id(id_especialidad)
        if not esp_actual:
            raise ValueError("La especialidad no existe.")

        nombre_input = datos.get("nombre")
        if not nombre_input:
            raise ValueError("El nombre no puede estar vacío.")

        nombre_norm = self._normalizar_texto(nombre_input)

        todas = self.service.obtener_todas()

        for esp in todas:
            if self._normalizar_texto(esp.nombre) == nombre_norm and esp.id_especialidad != id_especialidad:
                raise ValueError(f"Ya existe otra especialidad con el nombre '{esp.nombre}'.")

        esp_actual.nombre = nombre_input
        self.service.actualizar(esp_actual)
        return esp_actual

    def eliminar_especialidad(self, id_especialidad):
        esp = self.service.obtener_por_id(id_especialidad)
        if not esp:
            raise ValueError("La especialidad no existe.")
        self.service.eliminar(id_especialidad)

    def listar_especialidades(self):
        return self.service.obtener_todas()