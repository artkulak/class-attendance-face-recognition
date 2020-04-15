from flask import Flask, render_template, request, url_for, redirect, Response
import sqlite3
import datetime
import re
from Student import Student
from Lecturer import Lecturer
from DataGenerator import DataGenerator
import os
from Recognition import Recognizer
import shutil
from Trainer import Trainer
from embedding import emb
from sqlite3 import Error
import keras
from DatabaseInit import create_connection, DataBase

from warnings import filterwarnings
filterwarnings('ignore')

PROPERTIES = ['admin', 'lecturer', 'student']


create_connection("users.db")
create_connection("attendance.db")

app = Flask(__name__)

#------------------------------ LOGIN PART-------------------------------

@app.route('/')
def login():
    conn = sqlite3.connect('users.db').cursor()
    username = request.args.get('username')
    global USER_NAME
    global REAL_PROPERTY
    USER_NAME = username
    message = ''
    password = request.args.get('pass')
    if username != None and password != None:
        admin = conn.execute(f'''
        SELECT * FROM USERS
        WHERE user_name = '{username}'
        AND user_password = {password}
        AND user_property = '{PROPERTIES[0]}';
        ''')

        if len(admin.fetchall()) == 1:
            REAL_PROPERTY = PROPERTIES[0]
            return redirect(url_for('admin'))

        lecturer = conn.execute(f'''
                SELECT * FROM USERS
                WHERE user_name = '{username}'
                AND user_password = {password}
                AND user_property = '{PROPERTIES[1]}';
                ''')
        if len(lecturer.fetchall()) == 1:
            REAL_PROPERTY = PROPERTIES[1]
            return redirect(url_for('lecturer'))

        student = conn.execute(f'''
                        SELECT * FROM USERS
                        WHERE user_name = '{username}'
                        AND user_password = {password}
                        AND user_property = '{PROPERTIES[2]}';
                        ''')

        if len(student.fetchall()) == 1:
            return redirect(url_for('student'))

        message = 'Invalid data!'
    return render_template('login.html', message = message)


#------------------------------ ADMIN PART-------------------------------


@app.route('/admin')
def admin():
    global VIDEO
    VIDEO = False
    db = DataBase()
    if request.args.get('lect-create') == str(1):
        username = request.args.get('username')
        USR_VALID = True if re.match("^[A-Za-z]+$", username) else False
        pswrd = request.args.get('pass')
        PASS_VALID = True if re.match("^[0-9]+$", pswrd) else False
        mail = request.args.get('mail')
        MAIL_VALID = True if re.match("[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", mail) else False
        second_mail = request.args.get('second-mail')
        SCMAIL_VALID = True if re.match("[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", second_mail) else False

        if USR_VALID & PASS_VALID & MAIL_VALID & SCMAIL_VALID:
            name = request.args.get('username')
            dg = DataGenerator()
            #dg.generate(name)
            db.add_lecturer(username, int(pswrd), mail, second_mail)
        return redirect(url_for('admin'))
    elif request.args.get('lect-delete') == str(1):
        name = request.args.get('username')
        USR_VALID = True if re.match("^[A-Za-z]+$", name) else False
        if USR_VALID:
            for value in os.listdir('people/'):
                if name in value:
                    shutil.rmtree('people/' + value)

            db.delete_lecturer(request.args.get('username'))
        return redirect(url_for('admin'))
    elif request.args.get('stud-create') == str(1):
        username = request.args.get('username')
        USR_VALID = True if re.match("^[A-Za-z]+$", username) else False
        pswrd = request.args.get('pass')
        PASS_VALID = True if re.match("^[0-9]+$", pswrd) else False
        mail = request.args.get('mail')
        MAIL_VALID = True if re.match("[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", mail) else False
        second_mail = request.args.get('second-mail')
        SCMAIL_VALID = True if re.match("[a-z0-9._%+-]+@[a-z0-9.-]+\.[a-z]{2,}", second_mail) else False
        lect = request.args.get('lecturer')
        LECT_VALID = True if re.match("^[A-Za-z]+$", lect) else False

        if USR_VALID & PASS_VALID & MAIL_VALID & SCMAIL_VALID & LECT_VALID:
            name = request.args.get('username')
            dg = DataGenerator()
            dg.generate(name)
            db.add_student(username, int(pswrd), mail, second_mail, lect)
        return redirect(url_for('admin'))
    elif request.args.get('stud-delete') == str(1):
        name = request.args.get('username')
        USR_VALID = True if re.match("^[A-Za-z]+$", name) else False
        if USR_VALID:
            for value in os.listdir('people/'):
                if name in value:
                    shutil.rmtree('people/' + value)

            db.delete_student(request.args.get('username'))
        return redirect(url_for('admin'))
    studs = DataBase().get_all_students()
    lects = DataBase().get_all_lecturers()
    return render_template('admin.html', students = studs, lecturers = lects)

@app.route('/videostream', methods = ['POST', 'GET'])
def videostream():
    if VIDEO:
        rec = Recognizer()
        return Response(rec.Stream(), mimetype='multipart/x-mixed-replace; boundary=frame')
    return Response()


@app.route('/start_server', methods = ['POST', 'GET'])
def start_server():
    global VIDEO
    VIDEO = True
    studs = DataBase().get_all_students()
    lects = DataBase().get_all_lecturers()

    return render_template('admin.html', students = studs, lecturers = lects)


@app.route('/stop_server', methods = ['POST', 'GET'])
def stop_server():
    global VIDEO
    VIDEO = False

    studs = DataBase().get_all_students()
    lects = DataBase().get_all_lecturers()

    # return render_template('admin.html', students = studs, lecturers = lects)
    return redirect(url_for('admin'))


@app.route('/train_model', methods = ['POST', 'GET'])
def train_model():
    print('Training')
    trainer = Trainer()
    with keras.backend.get_session().graph.as_default():
        e = emb()
        trainer.train(e)
    return redirect(url_for('admin'))

#------------------------------ LECTURER PART-------------------------------

@app.route('/lecturer')
def lecturer():
    db = DataBase()
    if request.args.get('stud-add') == str(1):
        name = request.args.get('username')
        USR_VALID = True if re.match("^[A-Za-z]+$", name) else False
        if USR_VALID:
            db.add_student_lesson(USER_NAME, request.args.get('username'))
        return redirect(url_for('lecturer'))
    elif request.args.get('stud-delete') == str(1):
        name = request.args.get('username')
        USR_VALID = True if re.match("^[A-Za-z]+$", name) else False
        if USR_VALID:
            db.delete_student_lesson(USER_NAME, request.args.get('username'))
        return redirect(url_for('lecturer'))

    students = Lecturer(USER_NAME).get_students_vector()
    return render_template('lecturer.html', time = datetime.datetime.now().strftime('%b %d %Y %H:%M:%S'), students = students)

@app.route('/send_emails', methods = ['POST', 'GET'])
def send_emails():
    print('Sending...')
    Lecturer(USER_NAME).send_emails()
    return redirect(url_for('lecturer'))

@app.route('/get_attendance', methods = ['POST', 'GET'])
def get_attendance():
    db = DataBase()
    attendance = Recognizer().recognize(True)
    print(attendance)
    students = Lecturer(USER_NAME).get_students_vector(firsttime=False)
    for index, value in enumerate(students):
        if attendance[value[0]] > 0:
            #date = datetime.datetime.now().strftime("%Y-%m-%d")
            db.add_student_lesson(USER_NAME, value[0])
            #db.delete_student_lesson_fully(USER_NAME, value[0])
            #db.add_attendance(value[0], USER_NAME, date)

    students = Lecturer(USER_NAME).get_students_vector()
    return redirect(url_for('lecturer', studens = students))

#------------------------------ STUDENT PART-------------------------------

@app.route('/student')
def student():
    lects = Student(USER_NAME).get_lecturer_vector()
    attendance = Student(USER_NAME).get_attendance_vector()
    date = Student(USER_NAME).get_time_vector()
    id = Student(USER_NAME).get_id()
    for index, value in enumerate(attendance):
        if value == 1:
            attendance[index] = 'Was present'
        else:
            attendance[index] = 'Was absent'
    return render_template('student.html', id = id, student_name = USER_NAME, attendances = attendance, lecturers = lects, date = date)



if __name__ == '__main__':
    app.run(debug=True)
