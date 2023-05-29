
    CREATE SCHEMA IF NOT EXISTS student;

    #USE student;
    CREATE TABLE IF NOT EXISTS library_details (
        id_prestamo INT PRIMARY KEY AUTO_INCREMENT,
        titulo TEXT,
        isbn TEXT,
        autor TEXT,
        id_estudiante INTEGER UNIQUE NOT NULL
    );

    CREATE TABLE IF NOT EXISTS users_details (
        id INT PRIMARY KEY AUTO_INCREMENT,
        username TEXT,
        password TEXT
	);

    CREATE TABLE IF NOT EXISTS contact_details (
        id INT PRIMARY KEY AUTO_INCREMENT,
        firstname TEXT,
        surname TEXT,
        street_address TEXT,
        suburb TEXT
    );

    CREATE TABLE IF NOT EXISTS Asignaturas (
      asignatura_id INT PRIMARY KEY AUTO_INCREMENT,
      nombre VARCHAR(50)
    );

    CREATE TABLE IF NOT EXISTS Informes_Asignaturas (
      id INT PRIMARY KEY AUTO_INCREMENT,
      nombre VARCHAR(50),
      calificacion_media DECIMAL(3, 1)
    );

    CREATE TABLE IF NOT EXISTS Matriculas (
      id INT PRIMARY KEY AUTO_INCREMENT,
      estudiante_id INT UNIQUE,
      asignatura_id INT UNIQUE,
      calificacion DECIMAL(3, 1),
      fecha_modificacion TIMESTAMP,
      usuario_modificacion VARCHAR(50),
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

    DELIMITER $$

    CREATE PROCEDURE Generar_Informe_Asignaturas()
    BEGIN
        DECLARE done INT DEFAULT FALSE;
        DECLARE asignatura_id INT;
        DECLARE asignatura_nombre VARCHAR(255);
        DECLARE calificacion_media DECIMAL(5, 2);
        DECLARE cur CURSOR FOR
            SELECT Asignaturas.asignatura_id, Asignaturas.nombre, AVG(Matriculas.calificacion)
            FROM Asignaturas
            LEFT JOIN Matriculas ON Asignaturas.asignatura_id = Asignaturas.asignatura_id
            GROUP BY Asignaturas.asignatura_id;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET done = TRUE;

        TRUNCATE TABLE Informes_Asignaturas;

        OPEN cur;
        read_loop: LOOP
            FETCH cur INTO asignatura_id, asignatura_nombre, calificacion_media;
            IF done THEN
                LEAVE read_loop;
            END IF;
            INSERT INTO Informes_Asignaturas (id, nombre, calificacion_media)
            VALUES (asignatura_id, asignatura_nombre, calificacion_media);
        END LOOP;
        CLOSE cur;
    END $$

    DELIMITER ;

    CREATE TRIGGER Actualizar_Informes_Insert
    AFTER INSERT ON Matriculas
    FOR EACH ROW
    BEGIN
        CALL Generar_Informe_Asignaturas();
    END;

    CREATE TRIGGER Actualizar_Informes_Update
    AFTER UPDATE ON Matriculas
    FOR EACH ROW
    BEGIN
        CALL Generar_Informe_Asignaturas();
    END;

    CREATE TRIGGER Actualizar_Informes_Delete
    AFTER DELETE ON Matriculas
    FOR EACH ROW
    BEGIN
        CALL Generar_Informe_Asignaturas();
    END;
