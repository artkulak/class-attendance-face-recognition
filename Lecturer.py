import datetime
from datetime import date, timedelta
import sqlite3
from DatabaseInit import create_connection, DataBase
from Automail import Mailer
create_connection("users.db")
create_connection("attendance.db")

class Lecturer:
    def __init__(self, lecturer_name):
        self.mailer = Mailer()
        self.lecturer_name = lecturer_name
        self.usersdb = sqlite3.connect('users.db').cursor()
        self.attendancedb = sqlite3.connect('attendance.db').cursor()

    def get_students_vector(self, firsttime = True):
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        if firsttime:
            studs = self.usersdb.execute(f'''
            SELECT * FROM USERS
            WHERE lecturer = '{self.lecturer_name}'
            ''')

            db = DataBase()
            for value in studs.fetchall():
                notes = self.attendancedb.execute(f'''
                SELECT * FROM ATTENDANCE
                WHERE user_name = '{value[1]}'
                AND attendance_date = '{date}'
                ''').fetchall()

                if len(notes) == 0:
                    db.add_student_lesson(self.lecturer_name, value[1], 0)

        res = self.attendancedb.execute(f'''
        SELECT * FROM ATTENDANCE
        WHERE lecturer_name = '{self.lecturer_name}'
        AND attendance_date = '{date}'
        ''')
        students = []
        for value in res.fetchall():
            print(value)
            students.append([value[0],'Is Present' if value[2] == 1 else 'Is Absent'])
        return students

    def send_emails(self):
        date = datetime.datetime.now().strftime("%Y-%m-%d")

        res = self.attendancedb.execute(f'''
                SELECT user_name FROM ATTENDANCE
                WHERE lecturer_name = '{self.lecturer_name}'
                AND attendance_date = '{date}'
                AND present = 0
                ''')
        for value in res.fetchall():
            email = self.usersdb.execute(f'''
            SELECT user_parents_email FROM USERS
            WHERE user_name = '{value[0]}'
            ''').fetchall()[0]
            print(value[0], email[0])
            self.mailer.send(value[0], email[0])




