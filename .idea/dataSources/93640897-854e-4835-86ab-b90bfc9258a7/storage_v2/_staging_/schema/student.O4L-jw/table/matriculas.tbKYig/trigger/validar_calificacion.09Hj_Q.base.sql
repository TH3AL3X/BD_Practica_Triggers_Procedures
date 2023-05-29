create definer = root@localhost trigger Validar_Calificacion
    before insert
    on matriculas
    for each row
BEGIN
        IF NEW.calificacion < 0 THEN
            SET NEW.calificacion = 0;
        end if;
        IF NEW.calificacion > 10 THEN
            SET NEW.calificacion = 10;
        END IF;
    END;

