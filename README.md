# Sistema de Gestión de Turnos Médicos - Grupo 45

Este proyecto es una aplicación de escritorio integral desarrollada en **Python** con interfaz gráfica en **Tkinter** y persistencia en **SQLite**. El sistema administra el flujo completo de una clínica médica: desde la gestión de agendas y turnos, hasta la atención médica, emisión de recetas electrónicas, historia clínica y reportes gerenciales.

## 🏗 Arquitectura del Software

El proyecto implementa una arquitectura en capas basada en el patrón **MVC (Modelo-Vista-Controlador)**, desacoplando la lógica de negocio de la interfaz de usuario.

### Estructura de Directorios
*   **[`model/`](model/)**: Contiene las clases de entidad (POJOs) como `Paciente`, `Medico`, `Turno`, `Receta`. Estas clases solo transportan datos y no contienen lógica de negocio.
*   **[`view/`](view/)**: Interfaz gráfica construida con `tkinter`.
    *   Las vistas heredan de `tk.Frame` (para paneles integrados) o `tk.Toplevel` (para ventanas emergentes).
    *   Implementan lógica de UI avanzada como ordenamiento de tablas y validaciones visuales.
*   **[`controller/`](controller/)**: Actúa como intermediario. Recibe la entrada de la Vista, invoca la lógica del Servicio y actualiza la Vista.
*   **[`services/`](services/)**: Capa de Acceso a Datos (**DAO**) y Lógica de Negocio. Aquí se ejecutan las sentencias SQL y se validan reglas complejas (ej. solapamiento de horarios).
*   **[`img/`](img/)**: Recursos gráficos e iconos.

---

## 🛠 Patrones de Diseño Implementados

### 1. Singleton
*   **Ubicación:** [`services/database.py`](services/database.py)
*   **Descripción:** La clase `DatabaseConnection` garantiza que exista una **única instancia** de conexión a la base de datos SQLite durante todo el ciclo de vida de la aplicación.

### 2. DAO (Data Access Object)
*   **Ubicación:** Carpeta [`services/`](services/)
*   **Descripción:** Clases como `PacienteService` o `TurnoService` abstraen las operaciones CRUD. El resto de la aplicación interactúa con métodos de alto nivel sin conocer los detalles del SQL.

### 3. MVC (Model-View-Controller)
*   **Ubicación:** Estructura global del proyecto.
*   **Descripción:** Separación estricta de responsabilidades para facilitar el mantenimiento y la escalabilidad.

---

## 🚀 Funcionalidades Detalladas

### 1. Gestión Administrativa (ABM)
*   **Pacientes y Médicos:** Altas, bajas y modificaciones con validaciones estrictas.
*   **Especialidades:** Gestión del catálogo de especialidades médicas.
*   **Agenda Médica:** Configuración de horarios laborales y duración de turnos por profesional.

### 2. Gestión de Turnos (Mejorado)
Este módulo ha sido optimizado en [`view/turno_view.py`](view/turno_view.py) y [`controller/turno_controller.py`](controller/turno_controller.py):
*   **Reserva Inteligente:** Validación de disponibilidad basada en la agenda del médico.
*   **Filtros Avanzados:** Capacidad de filtrar el listado de turnos por **rango de fechas** (Desde/Hasta), permitiendo visualizar rápidamente la carga de trabajo de periodos específicos.
*   **Ordenamiento Dinámico:** La tabla de turnos permite **ordenar las columnas** (ID, Paciente, Médico, Fecha, Estado) de forma ascendente o descendente simplemente haciendo clic en los encabezados.
*   **Estados:** Flujo completo: *Pendiente -> Atendido / Cancelado / Ausente*.

### 3. Atención Médica y Recetas
*   **Registro de Atención:** Módulo para registrar diagnóstico, procedimiento e indicaciones.
*   **Recetas Electrónicas (PDF):**
    *   Generación automática de recetas en PDF con **ReportLab**.
    *   Lógica en [`controller/historia_clinica_controller.py`](controller/historia_clinica_controller.py).

### 4. Historia Clínica
*   Visualización cronológica de todas las atenciones de un paciente.
*   Acceso rápido a diagnósticos previos.

### 5. Reportes y Estadísticas
Módulo robusto en [`controller/reporte_controller.py`](controller/reporte_controller.py):
*   **Exportación:** Todos los reportes exportables a **CSV** y **PDF**.
*   **Tipos:** Turnos por Médico, Pacientes Atendidos, Turnos por Especialidad.
*   **Gráficos:** Gráfico de torta (Canvas) en [`view/reporte_estadistico_view.py`](view/reporte_estadistico_view.py) mostrando la distribución de estados de turnos.

### 6. Recordatorios Automáticos
*   **Email Service:** Integración con `smtplib` en [`services/email_service.py`](services/email_service.py).
*   **Funcionalidad:** Envío masivo de recordatorios a pacientes con turnos para el día siguiente.

### 7. Data Seeding
*   Clase [`services/data_seeder.py`](services/data_seeder.py) que puebla la base de datos con datos de prueba al iniciar el sistema por primera vez.

---

## 📦 Instalación y Ejecución

1.  **Requisitos:** Python 3.x.
2.  **Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ejecución:**
    ```bash
    python// filepath: d:\Gino Spadoni\Universidad\3°\DAO\TPI\TRABAJO-PRACTICO-DAO-GRUPO-45\README.md
# Sistema de Gestión de Turnos Médicos - Grupo 45

Este proyecto es una aplicación de escritorio integral desarrollada en **Python** con interfaz gráfica en **Tkinter** y persistencia en **SQLite**. El sistema administra el flujo completo de una clínica médica: desde la gestión de agendas y turnos, hasta la atención médica, emisión de recetas electrónicas, historia clínica y reportes gerenciales.

## 🏗 Arquitectura del Software

El proyecto implementa una arquitectura en capas basada en el patrón **MVC (Modelo-Vista-Controlador)**, desacoplando la lógica de negocio de la interfaz de usuario.

### Estructura de Directorios
*   **[`model/`](model/)**: Contiene las clases de entidad (POJOs) como `Paciente`, `Medico`, `Turno`, `Receta`. Estas clases solo transportan datos y no contienen lógica de negocio.
*   **[`view/`](view/)**: Interfaz gráfica construida con `tkinter`.
    *   Las vistas heredan de `tk.Frame` (para paneles integrados) o `tk.Toplevel` (para ventanas emergentes).
    *   Implementan lógica de UI avanzada como ordenamiento de tablas y validaciones visuales.
*   **[`controller/`](controller/)**: Actúa como intermediario. Recibe la entrada de la Vista, invoca la lógica del Servicio y actualiza la Vista.
*   **[`services/`](services/)**: Capa de Acceso a Datos (**DAO**) y Lógica de Negocio. Aquí se ejecutan las sentencias SQL y se validan reglas complejas (ej. solapamiento de horarios).
*   **[`img/`](img/)**: Recursos gráficos e iconos.

---

## 🛠 Patrones de Diseño Implementados

### 1. Singleton
*   **Ubicación:** [`services/database.py`](services/database.py)
*   **Descripción:** La clase `DatabaseConnection` garantiza que exista una **única instancia** de conexión a la base de datos SQLite durante todo el ciclo de vida de la aplicación.

### 2. DAO (Data Access Object)
*   **Ubicación:** Carpeta [`services/`](services/)
*   **Descripción:** Clases como `PacienteService` o `TurnoService` abstraen las operaciones CRUD. El resto de la aplicación interactúa con métodos de alto nivel sin conocer los detalles del SQL.

### 3. MVC (Model-View-Controller)
*   **Ubicación:** Estructura global del proyecto.
*   **Descripción:** Separación estricta de responsabilidades para facilitar el mantenimiento y la escalabilidad.

---

## 🚀 Funcionalidades Detalladas

### 1. Gestión Administrativa (ABM)
*   **Pacientes y Médicos:** Altas, bajas y modificaciones con validaciones estrictas.
*   **Especialidades:** Gestión del catálogo de especialidades médicas.
*   **Agenda Médica:** Configuración de horarios laborales y duración de turnos por profesional.

### 2. Gestión de Turnos (Mejorado)
Este módulo ha sido optimizado en [`view/turno_view.py`](view/turno_view.py) y [`controller/turno_controller.py`](controller/turno_controller.py):
*   **Reserva Inteligente:** Validación de disponibilidad basada en la agenda del médico.
*   **Filtros Avanzados:** Capacidad de filtrar el listado de turnos por **rango de fechas** (Desde/Hasta), permitiendo visualizar rápidamente la carga de trabajo de periodos específicos.
*   **Ordenamiento Dinámico:** La tabla de turnos permite **ordenar las columnas** (ID, Paciente, Médico, Fecha, Estado) de forma ascendente o descendente simplemente haciendo clic en los encabezados.
*   **Estados:** Flujo completo: *Pendiente -> Atendido / Cancelado / Ausente*.

### 3. Atención Médica y Recetas
*   **Registro de Atención:** Módulo para registrar diagnóstico, procedimiento e indicaciones.
*   **Recetas Electrónicas (PDF):**
    *   Generación automática de recetas en PDF con **ReportLab**.
    *   Lógica en [`controller/historia_clinica_controller.py`](controller/historia_clinica_controller.py).

### 4. Historia Clínica
*   Visualización cronológica de todas las atenciones de un paciente.
*   Acceso rápido a diagnósticos previos.

### 5. Reportes y Estadísticas
Módulo robusto en [`controller/reporte_controller.py`](controller/reporte_controller.py):
*   **Exportación:** Todos los reportes exportables a **CSV** y **PDF**.
*   **Tipos:** Turnos por Médico, Pacientes Atendidos, Turnos por Especialidad.
*   **Gráficos:** Gráfico de torta (Canvas) en [`view/reporte_estadistico_view.py`](view/reporte_estadistico_view.py) mostrando la distribución de estados de turnos.

### 6. Recordatorios Automáticos
*   **Email Service:** Integración con `smtplib` en [`services/email_service.py`](services/email_service.py).
*   **Funcionalidad:** Envío masivo de recordatorios a pacientes con turnos para el día siguiente.

### 7. Data Seeding
*   Clase [`services/data_seeder.py`](services/data_seeder.py) que puebla la base de datos con datos de prueba al iniciar el sistema por primera vez.

---

## 📦 Instalación y Ejecución

1.  **Requisitos:** Python 3.x.
2.  **Dependencias:**
    ```bash
    pip install -r requirements.txt
    ```
3.  **Ejecución:**
   Desde la raíz del proyecto:
    ```bash     
        python main.py
    ```