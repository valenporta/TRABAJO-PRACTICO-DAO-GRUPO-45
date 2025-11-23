
from services.paciente_service import PacienteService
from model.paciente import Paciente

class PacienteController:

    def __init__(self):
        self.service = PacienteService()

    # ---------------------------------------------------
    # Crear paciente (con todas las validaciones)
    # ---------------------------------------------------
    def crear_paciente(self, datos: dict):
        # Validaciones básicas
        if not datos.get("dni") or not datos["dni"].isdigit() or int(datos["dni"]) <= 0 or len(datos["dni"]) < 7:
            raise ValueError("El DNI es inválido. Debe ser un número positivo de al menos 7 dígitos.")

        if not datos.get("nombre"):
            raise ValueError("El nombre no puede estar vacío.")
        
        if any(char.isdigit() for char in datos["nombre"]):
            raise ValueError("El nombre no puede contener números.")

        if not datos.get("apellido"):
            raise ValueError("El apellido no puede estar vacío.")

        if any(char.isdigit() for char in datos["apellido"]):
            raise ValueError("El apellido no puede contener números.")

        # Verificar si el DNI ya existe
        existente = self.service.obtener_por_dni(datos["dni"])
        if existente:
            raise ValueError("Ya existe un paciente con ese DNI.")

        # Crear objeto Paciente
        paciente = Paciente(
            dni=datos["dni"],
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            telefono=datos.get("telefono"),
            email=datos.get("email"),
            fecha_nac=datos.get("fecha_nac")
        )

        # Guardar en BD
        return self.service.crear(paciente)

    # ---------------------------------------------------
    # Actualizar paciente
    # ---------------------------------------------------
    def actualizar_paciente(self, id_paciente, datos: dict):
        paciente = self.service.obtener_por_id(id_paciente)

        if paciente is None:
            raise ValueError("El paciente no existe.")

        # Validaciones
        if not datos.get("dni") or not datos["dni"].isdigit() or int(datos["dni"]) <= 0 or len(datos["dni"]) < 7:
            raise ValueError("El DNI es inválido. Debe ser un número positivo de al menos 7 dígitos.")

        if not datos.get("nombre"):
            raise ValueError("El nombre no puede estar vacío.")

        if any(char.isdigit() for char in datos["nombre"]):
            raise ValueError("El nombre no puede contener números.")

        if not datos.get("apellido"):
            raise ValueError("El apellido no puede estar vacío.")

        if any(char.isdigit() for char in datos["apellido"]):
            raise ValueError("El apellido no puede contener números.")

        # Validar que no haya otro paciente con ese DNI
        otro = self.service.obtener_por_dni(datos["dni"])
        if otro and otro.id_paciente != id_paciente:
            raise ValueError("Ya existe otro paciente con ese DNI.")

        # Actualizar datos
        paciente.dni = datos["dni"]
        paciente.nombre = datos["nombre"]
        paciente.apellido = datos["apellido"]
        paciente.telefono = datos.get("telefono")
        paciente.email = datos.get("email")
        paciente.fecha_nac = datos.get("fecha_nac")

        self.service.actualizar(paciente)
        return paciente

    # ---------------------------------------------------
    # Eliminar paciente
    # ---------------------------------------------------
    def eliminar_paciente(self, id_paciente):
        paciente = self.service.obtener_por_id(id_paciente)

        if paciente is None:
            raise ValueError("El paciente no existe.")

        self.service.eliminar(id_paciente)

    # ---------------------------------------------------
    # Obtener todos
    # ---------------------------------------------------
    def listar_pacientes(self):
        return self.service.obtener_todos()

    # ---------------------------------------------------
    # Obtener por DNI
    # ---------------------------------------------------
    def buscar_por_dni(self, dni):
        if not dni:
            raise ValueError("Debe ingresar un DNI.")

        return self.service.obtener_por_dni(dni)
