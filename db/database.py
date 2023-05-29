import sqlite3, mariadb, pymysql
from flask import current_app

db_locale = 'student.db'

def engine_sql():
    db_selected = current_app.config['DB_SELECTED']
    db_names_list = current_app.config['DB_NAMES']
    db_get = db_names_list[current_app.config['DB_SELECTED']]

    if(db_selected == 'sqlite'):
        return sqlite3.connect(db_get)
    elif(db_selected == 'mariadb'):
        return mariadb.connect(host=current_app.config['DB_HOST'],
                port=current_app.config['DB_PORT'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD'],
                database=db_get)
    elif(db_selected == 'mysql'):
        return pymysql.connect(host=current_app.config['DB_HOST'],
                port=current_app.config['DB_PORT'],
                user=current_app.config['DB_USER'],
                password=current_app.config['DB_PASSWORD'],
                database=db_get)

def create_database(sqlname):
    connie = engine_sql()
    c = connie.cursor()

    with open(f"db/{sqlname}", 'r') as sql_file:
        sql_script = sql_file.read()

    c.executescript(sql_script)

    connie.commit()
    connie.close()

class database():
    def remove_student(id):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""DELETE FROM contact_details WHERE id={0}""".format(id))
        connie.commit()
        connie.close()

    def insert_student(student_details):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""INSERT INTO contact_details (firstname, surname, street_address, suburb) VALUES (?, ?, ?, ?)""", student_details)
        connie.commit()
        connie.close()

    def remove_subject(id):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""DELETE FROM Asignaturas WHERE asignatura_id={0}""".format(id))
        connie.commit()
        connie.close()

    def remove_license(id):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""DELETE FROM Matriculas WHERE id={0}""".format(id))
        connie.commit()
        connie.close()

    def insert_subject(subject_details):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""INSERT INTO Asignaturas (nombre) VALUES (?)""", subject_details)
        connie.commit()
        connie.close()

    def find_subject(id):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""SELECT * FROM Asignaturas WHERE asignatura_id={0}""".format(id))
        for items in c.fetchall():
            return items

    def update_subject(subject_details):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""UPDATE Asignaturas SET nombre=? WHERE asignatura_id=?""", subject_details)
        connie.commit()
        connie.close()

    def check_if_user_exists(user_details):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""SELECT * FROM users_details""")
        for items in c.fetchall():
            if(items[1] == user_details):
                return True

    def get_user_details(username):
        connie = engine_sql()
        c = connie.cursor()

        if(current_app.config['DB_SELECTED'] == 'mysql'):
            c.execute("""SELECT * FROM users_details WHERE username=%s""", (username, ))
        else:
            c.execute("""SELECT * FROM users_details WHERE username=?""", username)
        for items in c.fetchall():
            return items

    def insert_user(user_details):
        connie = engine_sql()
        c = connie.cursor()

        if (current_app.config['DB_SELECTED'] == 'mysql'):
            c.execute("""INSERT INTO users_details (username, password) VALUES (%s, %s)""", (user_details, ))
        else:
            c.execute("""INSERT INTO users_details (username, password) VALUES (?, ?)""", user_details)

        c.execute("""INSERT INTO users_details (username, password) VALUES (?, ?)""", user_details)
        connie.commit()
        connie.close()

    def insert_library(library_details):
        connie = engine_sql()
        c = connie.cursor()
        if (current_app.config['DB_SELECTED'] == 'mysql'):
            c.execute("""INSERT INTO library_details (titulo, isbn, autor, id_estudiante) VALUES (%s, %s, %s, %s)""",
                      (library_details, ))
        else:
            c.execute("""INSERT INTO library_details (titulo, isbn, autor, id_estudiante) VALUES (?, ?, ?, ?)""", library_details)
        connie.commit()
        connie.close()

    def update_student(student_details):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""UPDATE contact_details SET firstname=?, surname=?, street_address=?, suburb=? WHERE id=?""", student_details)
        connie.commit()
        connie.close()

    def find_student(id):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""SELECT * FROM contact_details WHERE id={0}""".format(id))
        for items in c.fetchall():
            return items

    def check_if_exists(id):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""SELECT * FROM contact_details""")
        item = c.fetchall()
        if(type(item) is not None): return True

    def query_library(id):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""SELECT * FROM library_details WHERE id_estudiante=?""", id)
        library_data = c.fetchall()
        return library_data

    def find_subject_student(id):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""
        SELECT * FROM Matriculas WHERE estudiante_id={0}""".format(id))
        for items in c.fetchall():
            return items

    def insert_subject_student(subject_student_details):
        connie = engine_sql()
        c = connie.cursor()
        print(subject_student_details)
        c.execute("""INSERT INTO Matriculas (estudiante_id, asignatura_id, calificacion, fecha_modificacion, usuario_modificacion) 
        VALUES (?, ?, ?, ?, ?)""", subject_student_details)
        connie.commit()
        connie.close()

    def update_subject_student(subject_student_details):
        connie = engine_sql()
        c = connie.cursor()
        print(subject_student_details)
        c.execute("""UPDATE Matriculas SET estudiante_id=?, 
        asignatura_id=?, 
        calificacion=?, 
        fecha_modificacion=?, 
        usuario_modificacion=? WHERE id=?""", subject_student_details)
        connie.commit()
        connie.close()

    def query_licenses_plates_per_student(page, id):
        connie = engine_sql()
        c = connie.cursor()

        c.execute("""SELECT Matriculas.id, Matriculas.estudiante_id, Asignaturas.nombre, Matriculas.calificacion, Matriculas.fecha_modificacion, Matriculas.usuario_modificacion, Matriculas.asignatura_id FROM Matriculas INNER JOIN Asignaturas ON Asignaturas.asignatura_id=Matriculas.asignatura_id WHERE estudiante_id={0} LIMIT ?, ?""".format(id), page)
        student_data = c.fetchall()
        return student_data

    def query_ratings(page):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""SELECT DISTINCT nombre, calificacion_media FROM Informes_asignaturas LIMIT ?, ?""", page)
        ratings_data = c.fetchall()
        return ratings_data

    def query_subjects(page):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""SELECT * FROM Asignaturas LIMIT ?, ?""", page)
        student_data = c.fetchall()
        return student_data

    def query_contact_details(page):
        connie = engine_sql()
        c = connie.cursor()
        c.execute("""SELECT * FROM contact_details LIMIT ?, ?""", page)
        student_data = c.fetchall()
        return student_data