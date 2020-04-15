import sqlite3
import datetime
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to a SQLite database """
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)
    finally:
        conn.close()

class DataBase:

    def __init__(self):
        pass

    def add_lecturer(self, username, password, mail, secondmail):
        create_connection("users.db")
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        print(username)
        print(password)
        c.execute(f'''
                    INSERT INTO USERS VALUES ('lecturer', '{username}', {password}, '{mail}', '{secondmail}', '{None}');
        ''')
        conn.commit()

    def delete_lecturer(self, username):
        create_connection("users.db")
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(f'''
                            DELETE FROM USERS WHERE
                            user_name = '{username}'
                            AND user_property = 'lecturer'
                ''')
        conn.commit()

    def add_student(self, username, password, mail, parentmail, lecturer):
        create_connection("users.db")
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(f'''
                            INSERT INTO USERS VALUES ('student', '{username}', {password}, '{mail}', '{parentmail}', '{lecturer}');
                ''')
        conn.commit()

    def delete_student(self, username):
        create_connection("users.db")
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute(f'''
                                    DELETE FROM USERS WHERE
                                    user_name = '{username}'
                                    AND user_property = 'student'
                        ''')
        conn.commit()

    def add_student_lesson(self, lecturer, student, value = 1):
        create_connection("users.db")
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        res = c.execute(f'''SELECT * from USERS
               WHERE user_name = '{student}'
               ''')

        if len(res.fetchall()) > 0:
            create_connection("attendance.db")
            conn = sqlite3.connect('attendance.db')
            c = conn.cursor()
            date = datetime.datetime.now().strftime('%Y-%m-%d')
            exac = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
            if value == 0:
                c.execute(f'''
                               INSERT INTO attendance VALUES ('{student}', '{lecturer}', {value},'{date}', '{exac}');
                        ''')
            else:
                c.execute(f'''
                               UPDATE attendance 
                               SET present = 1
                               WHERE user_name = '{student}'
                               AND lecturer_name = '{lecturer}'
                               AND attendance_date = '{date}'
                        ''')
            conn.commit()


    def delete_student_lesson(self, lecturer, student):
        create_connection("users.db")
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        res = c.execute(f'''SELECT * from USERS
        WHERE user_name = '{student}'
        ''')


        if len(res.fetchall()) > 0:
            create_connection("attendance.db")
            conn = sqlite3.connect('attendance.db')
            c = conn.cursor()

            date = datetime.datetime.now().strftime('%Y-%m-%d')
            c.execute(f'''
                                           UPDATE attendance 
                                           SET present = 0
                                           WHERE user_name = '{student}'
                                           AND lecturer_name = '{lecturer}'
                                           AND attendance_date = '{date}'
                                    ''')
            conn.commit()


    def delete_student_lesson_fully(self, lecturer, student):
        create_connection("users.db")
        conn = sqlite3.connect('users.db')
        c = conn.cursor()

        res = c.execute(f'''SELECT * from USERS
           WHERE user_name = '{student}'
           ''')

        if len(res.fetchall()) > 0:
            create_connection("attendance.db")
            conn = sqlite3.connect('attendance.db')
            c = conn.cursor()

            date = datetime.datetime.now().strftime('%Y-%m-%d')
            c.execute(f'''
                                              DELETE FROM attendance 
                                              WHERE user_name = '{student}'
                                              AND lecturer_name = '{lecturer}'
                                              AND attendance_date = '{date}'
                                       ''')
            conn.commit()

    def get_all_students(self):
        create_connection("users.db")
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
        SELECT USER_NAME, USER_EMAIL, USER_PARENTS_EMAIL
        FROM USERS
        WHERE user_property = 'student';
        ''')

        studs = c.fetchall()
        students = []
        for stud in studs:
            students.append([stud[0], stud[1], stud[2]])
        return students

    def get_all_lecturers(self):
        create_connection("users.db")
        conn = sqlite3.connect('users.db')
        c = conn.cursor()
        c.execute('''
        SELECT USER_NAME, USER_EMAIL, USER_PARENTS_EMAIL
        FROM USERS
        WHERE user_property = 'lecturer';
        ''')

        lect = c.fetchall()
        lecturers = []
        for lc in lect:
            lecturers.append([lc[0], lc[1], lc[2]])
        return lecturers

    def create_usersdb(self):
        create_connection("users.db")
        conn = sqlite3.connect('users.db')  # You can create a new database by changing the name within the quotes
        c = conn.cursor()  # The database will be saved in the location where your 'py' file is saved

        # Create table - CLIENTS
        c.execute('''CREATE TABLE users
            (user_property varchar(255),
             user_name varchar(255),
             user_password number,
             user_email varchar(255),
             user_parents_email varchar(255),
             lecturer varchar(255)
            );''')

        # create admin
        c.execute(f'''
            INSERT INTO USERS VALUES ('admin', 'admin', 123456, 'art_kulak@mail.ru', 'art_kulak@mail.ru', '{None}');
            ''')

        conn.commit()

    def add_attendance(self, username, lecturer, date, value = 1):
        create_connection("attendance.db")
        conn = sqlite3.connect('attendance.db')  # You can create a new database by changing the name within the quotes
        c = conn.cursor()  # The database will be saved in the location where your 'py' file is saved
        exac = datetime.datetime.now().strftime("%Y-%m-%d-%H.%M.%S")
        c.execute(f'''
                INSERT INTO attendance VALUES ('{username}', '{lecturer}', {value},'{date}', '{exac}');
                ''')

        conn.commit()

    def create_attendancedb(self):
        create_connection("attendance.db")
        conn = sqlite3.connect('attendance.db')  # You can create a new database by changing the name within the quotes
        c = conn.cursor()  # The database will be saved in the location where your 'py' file is saved

        # Create table - CLIENTS
        c.execute('''CREATE TABLE attendance
                (user_name varchar(255),
                 lecturer_name varchar(255),
                 present number,
                 attendance_date date,
                 exact_date date);''')
        # c.execute('''
        #         INSERT INTO attendance VALUES ('penkins', 'jenkins', 1,'2019-08-10');
        #         ''')

        conn.commit()


if __name__ == '__main__':
    DataBase().create_usersdb()
    DataBase().create_attendancedb()
    print('Database created!')
