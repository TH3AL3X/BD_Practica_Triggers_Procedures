create definer = root@localhost trigger Validar_Calificacion
    before update
    on matriculas
    for each row
BEGIN
        IF NEW.calificacion < 0 THEN
            SET NEW.calificacion = 0;
        ELSEIF NEW.calificacion > 10 THEN
            SET NEW.calificacion = 10;
        END IF;
    END;

