from services.medico_service import MedicoService
from services.medico_especialidad_service import MedicoEspecialidadService
from model.medico import Medico

class MedicoController:

    def __init__(self):
        self.service = MedicoService()
        self.medico_especialidad_service = MedicoEspecialidadService()

    # Crear
    def crear_medico(self, datos: dict):
        # Validaciones para CREACIÓN (usando los métodos existentes del servicio)
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

        if not datos.get("matricula"):
            raise ValueError("La matrícula no puede estar vacía.")

        # Validar DNI único (usando el método existente)
        if self.service.obtener_por_dni(datos["dni"]):
            raise ValueError("Ya existe un médico con ese DNI.")

        # Validar matrícula única (usando el método existente)
        if self.service.obtener_por_matricula(datos["matricula"]):
            raise ValueError("Ya existe un médico con esa matrícula.")
        
        if not datos.get("id_especialidad"):
            raise ValueError("Debe seleccionarse una especialidad para el médico.")

        medico = Medico(
            dni=datos["dni"],
            nombre=datos["nombre"],
            apellido=datos["apellido"],
            matricula=datos["matricula"],
            telefono=datos.get("telefono"),
        )

        self.service.crear(medico)

        self.medico_especialidad_service.asignar(
        medico.id_medico,
        datos["id_especialidad"]
    )
        return medico   

    # Actualizar
    def actualizar_medico(self, id_medico, datos: dict):
        medico = self.service.obtener_por_id(id_medico)

        if not medico:
            raise ValueError("El médico no existe.")

        # --- VALIDACIONES DE DATOS (DNI, Nombre, Apellido, Matrícula) ---
        if not datos.get("dni") or not datos["dni"].isdigit() or int(datos["dni"]) <= 0 or len(datos["dni"]) < 7:
            raise ValueError("El DNI es inválido. Debe ser un número positivo de al menos 7 dígitos.")

        if not datos.get("nombre") or any(char.isdigit() for char in datos["nombre"]):
            raise ValueError("El nombre no puede estar vacío ni contener números.")

        if not datos.get("apellido") or any(char.isdigit() for char in datos["apellido"]):
            raise ValueError("El apellido no puede estar vacío ni contener números.")

        if not datos.get("matricula"):
            raise ValueError("La matrícula no puede estar vacía.")


        # ---------------------------------------------------------------
        # SOLUCIÓN: Usar métodos especializados que excluyen el ID actual
        # ---------------------------------------------------------------

        # DNI duplicado
        if self.service.dni_existe_en_otro_medico(datos["dni"], id_medico):
            raise ValueError("Otro médico ya tiene ese DNI.")

        # Matrícula duplicada
        if self.service.matricula_existe_en_otro_medico(datos["matricula"], id_medico):
            raise ValueError("Otro médico ya tiene esa matrícula.")
        # ---------------------------------------------------------------


        medico.dni = datos["dni"]
        medico.nombre = datos["nombre"]
        medico.apellido = datos["apellido"]
        medico.matricula = datos["matricula"]
        medico.telefono = datos.get("telefono")

        self.service.actualizar(medico) 

        # ---------------------------------------------------------------
        # 2. SOLUCIÓN: Actualizar la Especialidad en la tabla intermedia
        # ---------------------------------------------------------------
        id_especialidad_nuevo = datos.get("id_especialidad")
        
        if id_especialidad_nuevo is not None:
            # Eliminar la/s especialidad/es anterior/es del médico
            self.medico_especialidad_service.eliminar_por_medico(id_medico)
            
            # Asignar la nueva especialidad
            self.medico_especialidad_service.asignar(
                id_medico,
                id_especialidad_nuevo)
        return medico

    # Eliminar
    def eliminar_medico(self, id_medico):
        if not self.service.obtener_por_id(id_medico):
            raise ValueError("El médico no existe.")
        self.service.eliminar(id_medico)

    # Listar
    def listar_medicos(self):
        return self.service.obtener_todos()