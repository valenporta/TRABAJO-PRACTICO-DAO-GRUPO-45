# Plan de Acción - Sistema de Gestión de Turnos Médicos

Este documento detalla el estado actual del proyecto y los pasos necesarios para completar el desarrollo cumpliendo con los requerimientos solicitados.

## 1. Estado Actual del Proyecto

### Funcionalidades Implementadas
*   **Base de Datos:** Esquema completo definido en SQLite (tablas: paciente, medico, especialidad, agenda, turno, atencion, receta, historia_clinica).
*   **Patrón de Diseño:** Se utiliza el patrón **Singleton** en la clase `DatabaseConnection` (`services/database.py`) para gestionar una única conexión a la base de datos.
*   **Módulos ABM (Alta, Baja, Modificación):**
    *   Pacientes (MVC completo).
    *   Médicos (MVC completo).
    *   Especialidades (MVC completo).
*   **Menú Principal:** Estructura básica con acceso a los ABMs implementados.

### Arquitectura
El proyecto sigue el patrón arquitectónico **MVC (Modelo-Vista-Controlador)**:
*   `model/`: Definición de datos.
*   `view/`: Interfaz gráfica (Tkinter).
*   `controller/`: Lógica de interacción.
*   `services/`: Lógica de negocio y acceso a datos.

---

## 2. Funcionalidades Faltantes (To-Do List)

Para cumplir con los objetivos y alcances propuestos, se deben desarrollar los siguientes módulos:

### A. Gestión de Agenda Médica
*   **Objetivo:** Permitir definir la disponibilidad horaria de los médicos.
*   **Tareas:**
    1.  Crear `AgendaService`: Métodos para crear y consultar horarios por médico.
    2.  Crear `AgendaController` y `AgendaView`.
    3.  Validar que no se solapen horarios para un mismo médico.

### B. Gestión de Turnos (Asignación y Administración)
*   **Objetivo:** Registrar turnos verificando disponibilidad.
*   **Tareas:**
    1.  Crear `TurnoService`:
        *   Lógica para buscar horarios disponibles basándose en la `Agenda` y los `Turnos` ya ocupados.
        *   Validación de reglas de negocio (duración del turno, días laborables).
    2.  Crear `TurnoController` y `TurnoView`:
        *   Interfaz para seleccionar Especialidad -> Médico -> Fecha -> Horario Disponible.
    3.  **Gestión de Estados:** Implementar flujo de estados (Pendiente -> Atendido / Cancelado / Ausente).

### C. Atención Médica
*   **Objetivo:** Registrar el acto médico asociado a un turno.
*   **Tareas:**
    1.  Crear `AtencionService`, `AtencionController`, `AtencionView`.
    2.  Permitir seleccionar un turno "Pendiente" y cargar: Diagnóstico, Procedimiento, Indicaciones.
    3.  Al guardar, actualizar el estado del turno a "Atendido".

### D. Recetas
*   **Objetivo:** Emitir recetas vinculadas a una atención.
*   **Tareas:**
    1.  Integrar la carga de recetas en la vista de Atención Médica o como paso posterior.
    2.  Generar persistencia en la tabla `receta`.

### E. Historia Clínica
*   **Objetivo:** Visualizar el historial de un paciente.
*   **Tareas:**
    1.  Crear vista de Historia Clínica que agrupe: Datos del paciente + Lista de Atenciones (con sus diagnósticos y recetas).
    2.  Permitir búsqueda por DNI de paciente.

### F. Reportes y Estadísticas
*   **Objetivo:** Generar información para la toma de decisiones.
*   **Tareas:**
    1.  Crear módulo de reportes (puede ser una nueva pestaña o ventana).
    2.  **Reporte de Turnos:** Listados por fecha, médico o estado.
    3.  **Gráficos Estadísticos:** Ejemplo: Cantidad de turnos por especialidad (usando `matplotlib` si es posible, o conteos simples).

### G. Recordatorios de Turnos (Punto Crítico)
*   **Objetivo:** Gestionar recordatorios para turnos pendientes.
*   **Propuesta de Implementación:**
    *   **Alerta en Inicio:** Al abrir el sistema, mostrar una ventana o lista con los "Turnos del Día" o "Turnos de Mañana".
    *   **Visualización:** Destacar en la grilla de turnos aquellos próximos a vencer.

---

## 3. Plan de Implementación (Paso a Paso)

1.  **Agenda:** Implementar la carga de horarios para médicos. Sin esto no se pueden dar turnos.
2.  **Turnos:** Desarrollar la lógica de búsqueda de disponibilidad y reserva.
3.  **Integración en Main:** Agregar botones en `main.py` para "Gestión de Turnos" y "Agenda".
4.  **Atención y Recetas:** Desarrollar el flujo de atención del paciente.
5.  **Historia Clínica:** Vista de lectura de datos agregados.
6.  **Reportes y Recordatorios:** Agregados finales de valor.

## 4. Validación de Requerimientos Técnicos

*   **Patrón de Diseño:** Se cumple con el uso de **Singleton** en la conexión a BD. Se recomienda evaluar el uso de **Factory Method** si se requiere generar distintos tipos de reportes, o **Strategy** para filtros de búsqueda complejos, para enriquecer la arquitectura.
*   **Persistencia:** SQLite ya implementado.

---

**Nota:** Este archivo debe actualizarse a medida que se completen las tareas.
