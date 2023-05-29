from flask import Flask, render_template, request, session, redirect
import bcrypt
import db.database as database_querys
import datetime

app = Flask(__name__)
app.secret_key = "4eS9MRtY"

error_list = {
      "remove": "STUDENT HAS BEEN REMOVED SUCCESSFULLY!",
      "not_exists": "STUDENT DON'T EXISTS",
      "update": "STUDENT HAS BEEN UPDATED SUCCESSFULLY!",
      "update_subject": "SUBJECT HAS BEEN UPDATED SUCCESSFULLY!",
      "update_subject_student": "STUDENT SUBJECT HAS BEEN UPDATED SUCCESSFULLY!",
      "add_subject_student": "STUDENT SUBJECT HAS BEEN ADDED SUCCESSFULLY!",
      "library": "LIBRARY HAS BEEN ADDED SUCCESSFULLY!",
      "add": "STUDENT HAS BEEN ADDED SUCCESSFULLY! ",
      "add_subject": "SUBJECT HAS BEEN ADDED SUCCESSFULLY! ",
      "remove_subject": "SUBJECT HAS BEEN REMOVED SUCCESSFULLY!",
      "logged_in": "You need to logged in to use the tool",
      "invalid_login": "User not found or wrong password"
}

#   STUDENT
#   EDIT_STUDENT
#   ADD_STUDENT
#   REMOVE_STUDENT

@app.route('/')
@app.route('/student')
def student():
    app.config['title'] = "Student"
    if "logged_in" in session and session['logged_in'] is True:



        page = [(int(request.args.get('page', default=0)) - 1)*5+5, 5]
        next_page = int(request.args.get('page', default=0)) + 1
        previous_page = int(request.args.get('page', default=0)) - 1

        student_data = database_querys.database.query_contact_details(page)
        return render_template('student.html', student_data=student_data, next_page=next_page, previous_page=previous_page)
    else:
        return redirect('login')

@app.route('/student/add', methods = ['GET', 'POST'])
@app.route('/student/<int:id>/update', methods = ['GET', 'POST'])
def add_student(id = None):
    app.config['title'] = "Add Student"
    if "logged_in" in session and session['logged_in'] is True:
        if(id == None):
            if request.method == 'GET':
                return render_template('add_student.html', firstname="", surname="",
                                       street_address="", suburb="", type="add")
            else:
                database_querys.database.insert_student((request.form['firstname'], request.form['surname'], request.form['street_address'], request.form['suburb']))
                return render_template('success.html', type=error_list["add"])
        else:
            if request.method == 'GET':
                student_data = database_querys.database.find_student(id)
                return render_template('add_student.html', firstname=student_data[1], surname=student_data[2],
                                       street_address=student_data[3], suburb=student_data[4], type="update")
            elif request.method == 'PUT':
                database_querys.database.update_student((
                    request.args['firstname'],
                    request.args['surname'],
                    request.args['street_address'],
                    request.args['suburb'],
                    str(id)
                ))
                return render_template("success.html", type=error_list["update"])
    else:
        return redirect('login')

@app.route('/student/<int:id>/delete', methods = ['GET'])
def remove_student(id = None):
    app.config['title'] = "Remove Student"
    if "logged_in" in session and session['logged_in'] is True:
        #if request.method == 'GET':
        #    return render_template('remove.html')
        #else:

            if(database_querys.database.check_if_exists(id)):
                database_querys.database.remove_student(id)
                return render_template('success.html', type=error_list["remove"])
            else:
                return render_template('success.html', type=error_list["not_exists"])
    else:
        return redirect('login')

#   SUBJECTS
#   EDIT_SUBJECT
#   ADD_SUBJECT
#   REMOVE_SUBJECT

@app.route('/')
@app.route('/subject')
def subject():
    app.config['title'] = "Subject"
    if "logged_in" in session and session['logged_in'] is True:
        page = [(int(request.args.get('page', default=0)) - 1)*5+5, 5]
        next_page = int(request.args.get('page', default=0)) + 1
        previous_page = int(request.args.get('page', default=0)) - 1

        subject_data = database_querys.database.query_subjects(page)
        return render_template('subject.html', subject_data=subject_data, next_page=next_page, previous_page=previous_page)
    else:
        return redirect('login')

@app.route('/subject/add', methods = ['GET', 'POST'])
@app.route('/subject/<int:id>/update', methods = ['GET', 'POST'])
def add_subject(id = None):
    app.config['title'] = "Add Subject"
    if "logged_in" in session and session['logged_in'] is True:
        if (id == None):
            if request.method == 'GET':
                return render_template('add_subject.html', type="add")
            else:
                subject_details = [ request.form['name'] ]
                database_querys.database.insert_subject(subject_details)
                return render_template('success.html', type=error_list["add_subject"])
        else:
            if request.method == 'GET':
                subject_data = database_querys.database.find_subject(id)
                return render_template('add_subject.html', type="update", subject_name=subject_data[1])
            else:
                subject_details = [ request.form['name'], id ]
                database_querys.database.update_subject(subject_details)
                return render_template('success.html', type=error_list["update_subject"])
    else:
        return redirect('login')

@app.route('/subject/<int:id>/delete', methods = ['GET'])
def remove_subject(id = None):
    app.config['title'] = "Remove Subject"
    if "logged_in" in session and session['logged_in'] is True:
        #if request.method == 'GET':
        #    return render_template('remove.html')
        #else:
        database_querys.database.remove_subject(id)
        return render_template('success.html', type=error_list["remove_subject"])
    else:
        return redirect('login')

#   LICENSES
#   EDIT_LICENSE
#   ADD_LICENSE
#   REMOVE_LICENSE

@app.route('/license/<int:id_student>', methods = ['GET', 'POST'])
def license_student(id_student = None):
    app.config['title'] = "Licenses of student"
    if "logged_in" in session and session['logged_in'] is True:
        if request.method == 'GET':
            page = [(int(request.args.get('page', default=0)) - 1) * 5+5, 5]
            next_page = int(request.args.get('page', default=0)) + 1
            previous_page = int(request.args.get('page', default=0)) - 1

            subject_data = database_querys.database.query_licenses_plates_per_student(page, id_student)
            return render_template('subject_student.html', student_id=id_student, subject_data=subject_data, next_page=next_page,
                                   previous_page=previous_page)

@app.route('/license/<int:student_id>/add', methods = ['GET', 'POST'])
@app.route('/license/<int:id>/<int:student_id>/update', methods = ['GET', 'POST'])
def edit_subject_student(id = None, student_id = None):
    app.config['title'] = "Edit Subject of student"
    if "logged_in" in session and session['logged_in'] is True:
        if (id == None):
            if request.method == 'GET':
                subject_data = database_querys.database.find_subject_student(student_id)
                return render_template('add_subject_license.html', type="add")
            else:
                subject_data = [
                    student_id,
                    request.form['asignatura_id'],
                    request.form['calificacion'],
                    datetime.datetime.now(),
                    session['username']
                ]
                database_querys.database.insert_subject_student(subject_data)
                return render_template("success.html", type=error_list["add_subject_student"])
        else:
            if request.method == 'GET':
                subject_data = database_querys.database.find_subject_student(student_id)
                return render_template('add_subject_license.html',
                                       id=id,
                                       estudiante_id=subject_data[1],
                                       asignatura_id=subject_data[2],
                                       calificacion=subject_data[3],
                                       fecha_modificacion=subject_data[4],
                                       usuario_modificacion=subject_data[5],
                                       type="update")
            else:
                subject_data = [
                    request.form['estudiante_id'],
                    request.form['asignatura_id'],
                    request.form['calificacion'],
                    datetime.datetime.now(),
                    session['username'],
                    id
                ]
                database_querys.database.update_subject_student(subject_data)
                return render_template("success.html", type=error_list["update_subject_student"])
    else:
        return redirect('login')

#
# RATINGS
#
@app.route('/ratings', methods = ['GET', 'POST'])
def ratings():
    app.config['title'] = "Ratings"
    if "logged_in" in session and session['logged_in'] is True:
        if request.method == 'GET':
            page = [(int(request.args.get('page', default=0)) - 1) * 5+5, 5]
            next_page = int(request.args.get('page', default=0)) + 1
            previous_page = int(request.args.get('page', default=0)) - 1

            ratings_data = database_querys.database.query_ratings(page)
            return render_template('ratings.html', ratings_data=ratings_data, next_page=next_page, previous_page=previous_page)

""" DEPRECATED
@app.route('/library', methods = ['GET', 'POST'])
def library_page():
    app.config['title'] = "Library"
    if "logged_in" in session and session['logged_in'] is True:
        if request.method == 'GET':
            library_data = database_querys.database.query_library(request.args['id_estudiante'])
            return render_template("library.html", library_data=library_data)
        else:
            database_querys.database.insert_library((
                request.form['title'],
                request.form['isbn'],
                request.form['author'],
                request.form['id_estudiante']
            ))
            return render_template("success.html", type=error_list["library"])
    else:
        return redirect('login')
"""
#
#   LOGIN
#   REGISTER
#   LOGOUT

@app.route('/login', methods = ['GET', 'POST'])
def login():
    app.config['title'] = "Login"
    if request.method == 'GET':
        return render_template("login.html")
    else:
        login_username = [ request.form['username'] ]

        hashed_password = database_querys.database.get_user_details(login_username)[2].encode('utf-8')
        hashed_password_transform = request.form['password'].encode('utf-8')

        if(hashed_password is not None):
            if bcrypt.checkpw(hashed_password_transform, hashed_password):

                session['logged_in'] = True
                session['username'] = request.form['username']
                return redirect("student")
            else:
                return render_template("login.html", error=error_list["invalid_login"], error_show=True)
        else:
            return render_template("login.html", error=error_list["invalid_login"], error_show=True)

@app.route('/register', methods = ['GET', 'POST'])
def register():
    app.config['title'] = "Register"
    if request.method == 'GET':
        return render_template("register.html")
    else:
        if (database_querys.database.check_if_user_exists(request.form['username'])):
            return render_template("register.html", exists=True)
        else:
            hashed_password = bcrypt.hashpw(request.form['password'].encode('utf-8'), bcrypt.gensalt())

            database_querys.database.insert_user((
                request.form['username'],
                hashed_password
            ))
            session['logged_in'] = True
            return redirect("student")

@app.route('/logout', methods = ['GET', 'POST'])
def logout():
    session.clear()
    return redirect("login")