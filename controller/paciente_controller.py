from datetime import datetime
from services.paciente_service import PacienteService
from model.paciente import Paciente

class PacienteController:

    def __init__(self):
        self.service = PacienteService()

    def _validar_datos_adicionales(self, datos: dict):
        """
        Valida teléfono (solo números), email (@ y .com) y fecha de nacimiento (pasada).
        """
        # 1. Validar Teléfono (Si se ingresó algo, que sean solo números)
        telefono = datos.get("telefono")
        if telefono and not telefono.isdigit():
            raise ValueError("El teléfono solo puede contener números.")

        # 2. Validar Email (Debe tener '@' y terminar en '.com')
        email = datos.get("email")
        if email:
            if "@" not in email or not email.endswith(".com"):
                raise ValueError("El email es inválido (debe contener '@' y terminar en '.com').")

        # 3. Validar Fecha de Nacimiento (Debe ser menor a hoy)
        fecha_nac = datos.get("fecha_nac")
        if fecha_nac:
            try:
                # Asumimos formato YYYY-MM-DD que es el estándar de SQL/HTML
                fecha_dt = datetime.strptime(fecha_nac, "%Y-%m-%d")
                if fecha_dt >= datetime.now():
                    raise ValueError("La fecha de nacimiento debe ser anterior a la fecha actual.")
            except ValueError as e:
                # Si el error es nuestro (fecha futura), lo relanzamos
                if "anterior a la fecha actual" in str(e):
                    raise e
                # Si es error de formato
                raise ValueError("Formato de fecha inválido. Use AAAA-MM-DD.")

    # ---------------------------------------------------
    # Crear paciente (con todas las validaciones)
    # ---------------------------------------------------
    def crear_paciente(self, datos: dict):

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

        # NUEVAS VALIDACIONES (Teléfono, Email, Fecha)
        self._validar_datos_adicionales(datos)

        # VALIDACIÓN UNICIDAD para CREACIÓN
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

    def actualizar_paciente(self, id_paciente, datos: dict):
        # 1. Obtener el paciente a actualizar para verificar existencia
        paciente = self.service.obtener_por_id(id_paciente)
        if paciente is None:
            raise ValueError("El paciente no existe.")

        # 2. VALIDACIONES DE DATOS
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

        # NUEVAS VALIDACIONES (Teléfono, Email, Fecha)
        self._validar_datos_adicionales(datos)

        # 3. VALIDACIÓN DE DNI DUPLICADO
        if self.service.dni_existe_en_otro_paciente(dni_nuevo, id_paciente_a_excluir=id_paciente):
            raise ValueError("Ya existe otro paciente con ese DNI.")
        
        paciente.dni = dni_nuevo
        paciente.nombre = datos["nombre"]
        paciente.apellido = datos["apellido"]
        paciente.telefono = datos.get("telefono")
        paciente.email = datos.get("email")
        paciente.fecha_nac = datos.get("fecha_nac")

        self.service.actualizar(paciente)
        return paciente

    def eliminar_paciente(self, id_paciente):
        paciente = self.service.obtener_por_id(id_paciente)

        if paciente is None:
            raise ValueError("El paciente no existe.")

        self.service.eliminar(id_paciente)

    def listar_pacientes(self):
        return self.service.obtener_todos()

    def buscar_por_dni(self, dni):
        if not dni:
            raise ValueError("Debe ingresar un DNI.")

        return self.service.obtener_por_dni(dni)