
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
      estudiante_id INT,
      asignatura_id INT,
      calificacion DECIMAL(3, 1),
      fecha_modificacion TIMESTAMP,
      usuario_modificacion VARCHAR(50),
      FOREIGN KEY (estudiante_id) REFERENCES contact_details(id),
      FOREIGN KEY (asignatura_id) REFERENCES Asignaturas(asignatura_id)
    );

    CREATE TRIGGER IF NOT EXISTS Validar_Calificacion_Insert
    BEFORE INSERT ON Matriculas
    FOR EACH ROW
    BEGIN
        IF NEW.calificacion < 0 THEN
            SET NEW.calificacion = 0;
        end if;
        IF NEW.calificacion > 10 THEN
            SET NEW.calificacion = 10;
        END IF;
    END;

    CREATE TRIGGER IF NOT EXISTS Validar_Calificacion_Update
    BEFORE UPDATE ON Matriculas
    FOR EACH ROW
    BEGIN
        IF NEW.calificacion < 0 THEN
            SET NEW.calificacion = 0;
        end if;
        IF NEW.calificacion > 10 THEN
            SET NEW.calificacion = 10;
        END IF;
    END;

    DROP PROCEDURE Insertar_Informes;

    DELIMITER $$

    CREATE PROCEDURE Insertar_Informes()
    BEGIN
        DECLARE completado INT DEFAULT FALSE;
        DECLARE nombre VARCHAR(50);
        DECLARE calificacion_media FLOAT;

        DECLARE datos_asignaturas CURSOR FOR
            SELECT Asignaturas.nombre, AVG(Matriculas.calificacion) FROM Asignaturas
               INNER JOIN Matriculas ON Asignaturas.asignatura_id = Asignaturas.asignatura_id GROUP BY Asignaturas.asignatura_id;
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET completado = TRUE;

        DELETE FROM informes_asignaturas WHERE id<0;

        OPEN datos_asignaturas;
        read_loop: LOOP
            FETCH datos_asignaturas INTO nombre, calificacion_media;
            IF completado THEN
              LEAVE read_loop;
            END IF;
            INSERT INTO informes_asignaturas (nombre, calificacion_media) VALUES (nombre, calificacion_media);
        end loop;

        CLOSE datos_asignaturas;

    END $$

    DELIMITER ;

    CREATE TRIGGER IF NOT EXISTS Insertar_Informes_Updates
        BEFORE UPDATE ON Matriculas
        FOR EACH ROW
        BEGIN
            call Insertar_Informes();
    END;

    CREATE TRIGGER IF NOT EXISTS Insertar_Informes_Updates
        AFTER INSERT ON Matriculas
        FOR EACH ROW
        BEGIN
            call Insertar_Informes();
    END;

