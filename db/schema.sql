
PRAGMA foreign_keys = ON;

BEGIN TRANSACTION;

DROP TRIGGER IF EXISTS turnos_updated_at;
DROP TRIGGER IF EXISTS recetas_set_numero;

DROP TABLE IF EXISTS historial_clinico;
DROP TABLE IF EXISTS recetas;
DROP TABLE IF EXISTS turnos;
DROP TABLE IF EXISTS agenda_semanal;
DROP TABLE IF EXISTS medico_especialidad;
DROP TABLE IF EXISTS medicos;
DROP TABLE IF EXISTS especialidades;
DROP TABLE IF EXISTS pacientes;

CREATE TABLE pacientes (
  id                INTEGER PRIMARY KEY,
  dni               TEXT    NOT NULL UNIQUE,
  nombre            TEXT    NOT NULL,
  apellido          TEXT    NOT NULL,
  fecha_nacimiento  TEXT    NOT NULL,
  sexo              TEXT    NOT NULL CHECK (sexo IN ('F','M','X')),
  telefono          TEXT,
  email             TEXT,
  notas             TEXT,
  activo            INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0,1))
);
CREATE INDEX idx_pacientes_apellido_nombre ON pacientes(apellido, nombre);

CREATE TABLE especialidades (
  id          INTEGER PRIMARY KEY,
  nombre      TEXT NOT NULL UNIQUE,
  descripcion TEXT,
  activa      INTEGER NOT NULL DEFAULT 1 CHECK (activa IN (0,1))
);

CREATE TABLE medicos (
  id         INTEGER PRIMARY KEY,
  matricula  TEXT NOT NULL UNIQUE,
  nombre     TEXT NOT NULL,
  apellido   TEXT NOT NULL,
  telefono   TEXT,
  email      TEXT,
  activo     INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0,1))
);
CREATE INDEX idx_medicos_apellido_nombre ON medicos(apellido, nombre);

CREATE TABLE medico_especialidad (
  medico_id        INTEGER NOT NULL,
  especialidad_id  INTEGER NOT NULL,
  PRIMARY KEY (medico_id, especialidad_id),
  FOREIGN KEY (medico_id)       REFERENCES medicos(id)        ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (especialidad_id) REFERENCES especialidades(id) ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE agenda_semanal (
  id          INTEGER PRIMARY KEY,
  medico_id   INTEGER NOT NULL,
  dia_semana  INTEGER NOT NULL CHECK (dia_semana BETWEEN 0 AND 6),
  hora_inicio TEXT    NOT NULL,
  hora_fin    TEXT    NOT NULL,
  activo      INTEGER NOT NULL DEFAULT 1 CHECK (activo IN (0,1)),
  FOREIGN KEY (medico_id) REFERENCES medicos(id) ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE INDEX idx_agenda_medico_dia ON agenda_semanal(medico_id, dia_semana);

CREATE TABLE turnos (
  id                       INTEGER PRIMARY KEY,
  medico_id                INTEGER NOT NULL,
  paciente_id              INTEGER NOT NULL,
  fecha_hora               TEXT    NOT NULL,
  duracion_min             INTEGER NOT NULL DEFAULT 30 CHECK (duracion_min > 0 AND duracion_min <= 480),
  estado                   TEXT    NOT NULL CHECK (estado IN ('reservado','confirmado','atendido','ausente','cancelado')),
  recordatorio_24h_enviado INTEGER NOT NULL DEFAULT 0 CHECK (recordatorio_24h_enviado IN (0,1)),
  recordatorio_2h_enviado  INTEGER NOT NULL DEFAULT 0 CHECK (recordatorio_2h_enviado  IN (0,1)),
  created_at               TEXT    NOT NULL DEFAULT (datetime('now')),
  updated_at               TEXT    NOT NULL DEFAULT (datetime('now')),
  especialidad_id          INTEGER REFERENCES especialidades(id),
  UNIQUE(medico_id, fecha_hora),
  FOREIGN KEY (medico_id)   REFERENCES medicos(id)   ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE RESTRICT ON UPDATE CASCADE
);
CREATE INDEX idx_turnos_medico_fecha ON turnos(medico_id, fecha_hora);
CREATE INDEX idx_turnos_paciente_fecha ON turnos(paciente_id, fecha_hora);

CREATE TRIGGER turnos_updated_at
AFTER UPDATE ON turnos
FOR EACH ROW
WHEN NEW.updated_at = OLD.updated_at
BEGIN
  UPDATE turnos SET updated_at = datetime('now') WHERE id = OLD.id;
END;

CREATE TABLE historial_clinico (
  id          INTEGER PRIMARY KEY,
  turno_id    INTEGER NOT NULL UNIQUE,
  paciente_id INTEGER NOT NULL,
  medico_id   INTEGER NOT NULL,
  fecha       TEXT    NOT NULL,
  motivo      TEXT    NOT NULL,
  diagnostico TEXT    NOT NULL,
  indicaciones TEXT,
  FOREIGN KEY (turno_id)    REFERENCES turnos(id)     ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (paciente_id) REFERENCES pacientes(id)  ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (medico_id)   REFERENCES medicos(id)    ON DELETE RESTRICT ON UPDATE CASCADE
);

CREATE TABLE recetas (
  id          INTEGER PRIMARY KEY,
  numero      INTEGER UNIQUE,
  fecha       TEXT    NOT NULL,
  medico_id   INTEGER NOT NULL,
  paciente_id INTEGER NOT NULL,
  turno_id    INTEGER,
  contenido   TEXT    NOT NULL,
  observaciones TEXT,
  FOREIGN KEY (medico_id)   REFERENCES medicos(id)   ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (paciente_id) REFERENCES pacientes(id) ON DELETE RESTRICT ON UPDATE CASCADE,
  FOREIGN KEY (turno_id)    REFERENCES turnos(id)    ON DELETE SET NULL ON UPDATE CASCADE
);

CREATE TRIGGER recetas_set_numero
AFTER INSERT ON recetas
FOR EACH ROW
WHEN NEW.numero IS NULL
BEGIN
  UPDATE recetas SET numero = NEW.id WHERE id = NEW.id;
END;

-- Seeds
INSERT INTO especialidades (nombre, descripcion) VALUES
 ('Clínica Médica','Atención integral de adultos'),
 ('Pediatría','Niñez y adolescencia'),
 ('Cardiología','Sistema cardiovascular'),
 ('Dermatología','Piel y anexos'),
 ('Traumatología','Sistema músculo-esquelético');

INSERT INTO medicos (matricula, nombre, apellido, telefono, email) VALUES
 ('10001','Carlos','Sánchez','351-555-1001','csanchez@example.com'),
 ('10002','Laura','Romero','351-555-1002','lromero@example.com'),
 ('10003','Martín','Álvarez','351-555-1003','malvarez@example.com');

INSERT INTO medico_especialidad (medico_id, especialidad_id) VALUES
 (1,1),(1,3),
 (2,2),(2,4),
 (3,5);

INSERT INTO agenda_semanal (medico_id, dia_semana, hora_inicio, hora_fin) VALUES
 (1,0,'09:00','17:00'),(1,1,'09:00','17:00'),(1,2,'09:00','17:00'),(1,3,'09:00','17:00'),(1,4,'09:00','17:00'),
 (2,0,'09:00','17:00'),(2,1,'09:00','17:00'),(2,2,'09:00','17:00'),(2,3,'09:00','17:00'),(2,4,'09:00','17:00'),
 (3,0,'09:00','17:00'),(3,1,'09:00','17:00'),(3,2,'09:00','17:00'),(3,3,'09:00','17:00'),(3,4,'09:00','17:00');

INSERT INTO pacientes (dni, nombre, apellido, fecha_nacimiento, sexo, telefono, email, notas) VALUES
 ('30123456','Juan','Pérez','1990-05-10','M','351-600-0001','juan.perez@example.com',NULL),
 ('31234567','María','Gómez','1988-11-22','F','351-600-0002','maria.gomez@example.com',NULL),
 ('32345678','Luis','López','1975-07-01','M','351-600-0003','luis.lopez@example.com','Hipertensión controlada'),
 ('33456789','Ana','Torres','2001-09-15','F','351-600-0004','ana.torres@example.com',NULL),
 ('34567890','Sofía','Díaz','1995-03-30','F','351-600-0005','sofia.diaz@example.com',NULL);

INSERT INTO turnos (medico_id, paciente_id, fecha_hora, estado, especialidad_id) VALUES
 (1,1,'2025-10-27 09:00','reservado', 1),
 (1,2,'2025-10-27 09:30','confirmado', 1),
 (2,3,'2025-10-27 10:00','atendido',  2),
 (3,4,'2025-10-28 11:00','cancelado', 5),
 (2,5,'2025-10-29 12:00','confirmado',2),
 (1,3,'2025-10-29 12:30','atendido',  3),
 (3,1,'2025-10-30 15:00','ausente',   5),
 (1,4,'2025-10-30 15:30','reservado', 3),
 (2,2,'2025-10-31 16:00','confirmado',2),
 (3,5,'2025-10-31 16:30','reservado', 5);

COMMIT;
