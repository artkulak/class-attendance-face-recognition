import datetime
from datetime import date, timedelta
import sqlite3
from DatabaseInit import create_connection
create_connection("users.db")
create_connection("attendance.db")

class Student:

    def __init__(self, user_name):
        self.user_name = user_name
        self.usersdb = sqlite3.connect('users.db').cursor()
        self.attendancedb = sqlite3.connect('attendance.db').cursor()

    def get_lecturer_vector(self):
        lecturer_vector = []

        lecturer = self.usersdb.execute(
            f'''
            SELECT lecturer FROM USERS
            WHERE user_name = '{self.user_name}'
            '''
        )

        lects = [lecturer.fetchall()[0][0]]*5
        return lects

    def get_attendance_vector(self):
        attendance_vector = [2,2,2,2,2]
        dates = []
        curdate = datetime.datetime.now()
        # curdate = date(year = 2019, month=8, day = 4)
        if curdate.weekday() + 1 == 6:
            attendance_vector = [0,0,0,0,0]
            for i in range(5):
                date = (curdate - timedelta((5-i))).strftime('%Y-%m-%d')
                dates.append(date)
        elif curdate.weekday() + 1 == 7:
            attendance_vector = [0,0,0,0,0]
            for i in range(5):
                date = (curdate - timedelta((5-i) + 1)).strftime('%Y-%m-%d')
                dates.append(date)
        else:
            val = curdate.weekday()+1
            for i in range(val):
                attendance_vector[i] = 0
                date = (curdate - timedelta((val - i) - 1)).strftime('%Y-%m-%d')

                dates.append(date)
        for index, dt in enumerate(dates):
            attended = self.attendancedb.execute(
            f'''
            SELECT * FROM ATTENDANCE
            WHERE user_name = '{self.user_name}'
            AND attendance_date = '{dt}'
            AND present = 1
            '''
            )

            if len(attended.fetchall()) > 0:
                attendance_vector[index] = 1

        return attendance_vector

    def get_time_vector(self):
        attendance_vector = [2, 2, 2, 2, 2]
        dates = []
        curdate = datetime.datetime.now()
        # curdate = date(year = 2019, month=8, day = 4)
        if curdate.weekday() + 1 == 6:
            attendance_vector = [0, 0, 0, 0, 0]
            for i in range(5):
                date = (curdate - timedelta((5 - i))).strftime('%Y-%m-%d')
                dates.append(date)
        elif curdate.weekday() + 1 == 7:
            attendance_vector = [0, 0, 0, 0, 0]
            for i in range(5):
                date = (curdate - timedelta((5 - i) + 1)).strftime('%Y-%m-%d')
                dates.append(date)
        else:
            val = curdate.weekday() + 1
            for i in range(val):
                attendance_vector[i] = 0
                date = (curdate - timedelta((val - i) - 1)).strftime('%Y-%m-%d')

                dates.append(date)

        exec_dates = []
        for index, dt in enumerate(dates):
            attended = self.attendancedb.execute(
                f'''
                SELECT * FROM ATTENDANCE
                WHERE user_name = '{self.user_name}'
                AND attendance_date = '{dt}'
                AND present = 1
                '''
            )
            try:
                exec_dates.append(attended.fetchall()[0][-1])
            except:
                exec_dates.append('Not attended')
        return exec_dates

    def get_id(self):
        users = self.usersdb.execute(
            f'''
            SELECT user_name FROM USERS
            '''
        )
        items = []
        for value in users.fetchall():
            items.append(value[0])

        for index, it in enumerate(sorted(items)):
            if it == self.user_name:
                return index


