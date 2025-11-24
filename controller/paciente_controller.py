from services.paciente_service import PacienteService
from model.paciente import Paciente

class PacienteController:

    def __init__(self):
        self.service = PacienteService()

    # ---------------------------------------------------
    # Crear paciente (con todas las validaciones)
    # ---------------------------------------------------
    def crear_paciente(self, datos: dict):
        # Validaciones básicas (DNI)
        if not datos.get("dni") or not datos["dni"].isdigit() or int(datos["dni"]) <= 0 or len(datos["dni"]) < 7:
            raise ValueError("El DNI es inválido. Debe ser un número positivo de al menos 7 dígitos.")

        # Validaciones básicas (Nombre y Apellido)
        if not datos.get("nombre"):
            raise ValueError("El nombre no puede estar vacío.")
        if any(char.isdigit() for char in datos["nombre"]):
            raise ValueError("El nombre no puede contener números.")

        if not datos.get("apellido"):
            raise ValueError("El apellido no puede estar vacío.")
        if any(char.isdigit() for char in datos["apellido"]):
            raise ValueError("El apellido no puede contener números.")

        # VALIDACIÓN UNICIDAD para CREACIÓN
        # Usamos obtener_por_dni (que devuelve un objeto Paciente) para verificar existencia
        if self.service.obtener_por_dni(datos["dni"]):
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
        # 1. Obtener el paciente a actualizar para verificar existencia
        paciente = self.service.obtener_por_id(id_paciente)
        if paciente is None:
            raise ValueError("El paciente no existe.")

        # 2. VALIDACIONES DE DATOS (DNI, Nombre, Apellido)
        dni_nuevo = datos["dni"]
        
        # Validación DNI
        if not dni_nuevo or not dni_nuevo.isdigit() or int(dni_nuevo) <= 0 or len(dni_nuevo) < 7:
            raise ValueError("El DNI es inválido. Debe ser un número positivo de al menos 7 dígitos.")
            
        # Validación Nombre
        if not datos.get("nombre") or any(char.isdigit() for char in datos["nombre"]):
            raise ValueError("El nombre no puede estar vacío ni contener números.")

        # Validación Apellido
        if not datos.get("apellido") or any(char.isdigit() for char in datos["apellido"]):
            raise ValueError("El apellido no puede estar vacío ni contener números.")


        # 3. VALIDACIÓN DE DNI DUPLICADO (SOLUCIÓN: Usamos el método especializado del servicio)
        
        # Si el DNI nuevo ya existe en OTRO paciente, lanza error.
        if self.service.dni_existe_en_otro_paciente(dni_nuevo, id_paciente_a_excluir=id_paciente):
            raise ValueError("Ya existe otro paciente con ese DNI.")
        
        # 4. Actualizar datos en el objeto y la BD
        paciente.dni = dni_nuevo
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