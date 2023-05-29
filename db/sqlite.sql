
    CREATE TABLE IF NOT EXISTS library_details (
        id_prestamo INTEGER PRIMARY KEY AUTOINCREMENT,
        titulo TEXT,
        isbn TEXT,
        autor TEXT,
        id_estudiante INTEGER UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS users_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE,
        password TEXT
	);

    CREATE TABLE IF NOT EXISTS contact_details (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        firstname TEXT,
        surname TEXT,
        street_address TEXT,
        suburb TEXT
    );

    CREATE TABLE IF NOT EXISTS Asignaturas (
      asignatura_id INTEGER PRIMARY KEY AUTOINCREMENT,
      nombre VARCHAR(50)
    );

    CREATE TABLE IF NOT EXISTS Matriculas (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      estudiante_id INT,
      asignatura_id INT,
      calificacion DECIMAL(3, 1),
      fecha_modificacion TIMESTAMP,
      usuario_modificacion VARCHAR(50),
      PRIMARY KEY (estudiante_id, asignatura_id),
      FOREIGN KEY (estudiante_id) REFERENCES contact_details(id),
      FOREIGN KEY (asignatura_id) REFERENCES Asignaturas(asignatura_id)
    );

    CREATE TRIGGER IF NOT EXISTS Validar_Calificacion_Insert
    AFTER INSERT ON Matriculas
    FOR EACH ROW
    BEGIN
        UPDATE Matriculas SET calificacion =
            CASE
                WHEN NEW.calificacion < 0 THEN 0
                WHEN NEW.calificacion > 10 THEN 10
                ELSE NEW.calificacion
            END
        WHERE id = NEW.id;
    END;

    CREATE TRIGGER IF NOT EXISTS Validar_Calificacion
    AFTER UPDATE ON Matriculas
    FOR EACH ROW
    BEGIN
        UPDATE Matriculas SET calificacion =
            CASE
                WHEN NEW.calificacion < 0 THEN 0
                WHEN NEW.calificacion > 10 THEN 10
                ELSE NEW.calificacion
            END
        WHERE id = NEW.id;
    END;

