from faker import Faker
import random
import sqlite3

fake = Faker()

class CreateConnection:
    def __init__(self, db_name):
        self.conn = sqlite3.connect(db_name)
        self.cur = self.conn.cursor()

    def close_connection(self):
        self.conn.close()
        print("Connection closed.")
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_type is not None:
            self.conn.rollback()
        else:
            self.conn.commit()
        self.conn.close()
        print("Connection closed.")

class CreateTables:
    def __init__(self, connection):
        self.conn = connection
        self.cur = connection.cur

    def create_tables(self):
        self.cur.execute('''CREATE TABLE IF NOT EXISTS students (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            group_id INTEGER,
                            FOREIGN KEY (group_id) REFERENCES groups(id))''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS groups (
                            id INTEGER PRIMARY KEY,
                            name TEXT)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS lecturers (
                            id INTEGER PRIMARY KEY,
                            name TEXT)''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS subjects (
                            id INTEGER PRIMARY KEY,
                            name TEXT,
                            lecturer_id INTEGER,
                            FOREIGN KEY (lecturer_id) REFERENCES lecturers(id))''')
        self.cur.execute('''CREATE TABLE IF NOT EXISTS grades (
                            id INTEGER PRIMARY KEY,
                            student_id INTEGER,
                            subject_id INTEGER,
                            grade INTEGER,
                            date TEXT,
                            FOREIGN KEY (student_id) REFERENCES students(id),
                            FOREIGN KEY (subject_id) REFERENCES subjects(id))''')
        self.conn.conn.commit()

class InsertData:
    def __init__(self, connection):
        self.conn = connection
        self.cur = connection.cur

    def insert_group(self, name):
        self.cur.execute("INSERT INTO groups (name) VALUES (?)", (name,))
        self.conn.conn.commit()
        return self.cur.lastrowid

    def insert_student(self, name, group_id):
        self.cur.execute("INSERT INTO students (name, group_id) VALUES (?, ?)", (name, group_id))
        self.conn.conn.commit()
        return self.cur.lastrowid

    def insert_lecturer(self, name):
        self.cur.execute("INSERT INTO lecturers (name) VALUES (?)", (name,))
        self.conn.conn.commit()
        return self.cur.lastrowid

    def insert_subject(self, name, lecturer_id):
        self.cur.execute("INSERT INTO subjects (name, lecturer_id) VALUES (?, ?)", (name, lecturer_id))
        self.conn.conn.commit()
        return self.cur.lastrowid

    def insert_grade(self, student_id, subject_id, grade, date):
        self.cur.execute("INSERT INTO grades (student_id, subject_id, grade, date) VALUES (?, ?, ?, ?)", (student_id, subject_id, grade, date))
        self.conn.conn.commit()

    def generate_fake_data(self):
        groups = ['Group A', 'Group B', 'Group C']
        lecturers = [fake.name() for _ in range(5)]
        subjects = ['Mathematics', 'Physics', 'Chemistry', 'Biology', 'History', 'Geography', 'English', 'Computer Science']
        students = [(fake.name(), random.choice(groups)) for _ in range(30)] 

        grades = []
        for student in students:
            for subject in subjects:
                for _ in range(random.randint(5, 20)):
                    grade = random.randint(1, 6)
                    date = fake.date_this_year(before_today=True, after_today=False)
                    grades.append((student[0], subject, grade, date))

        return groups, lecturers, subjects, students, grades

    def insert_fake_data(self):
        groups, lecturers, subjects, students, grades = self.generate_fake_data()

        group_ids = {}
        for group in groups:
            group_id = self.insert_group(group)
            group_ids[group] = group_id

        lecturer_ids = {}
        for lecturer in lecturers:
            lecturer_id = self.insert_lecturer(lecturer)
            lecturer_ids[lecturer] = lecturer_id

        subject_ids = {}
        for subject, lecturer_id in zip(subjects, lecturer_ids.values()):
            subject_id = self.insert_subject(subject, lecturer_id)
            subject_ids[subject] = subject_id

        student_ids = {}
        for student, group in students:
            student_id = self.insert_student(student, group_ids[group])
            student_ids[student] = student_id

        for grade in grades:
            student_id = student_ids[grade[0]]
            subject_id = subject_ids[grade[1]]
            self.insert_grade(student_id, subject_id, grade[2], grade[3].strftime('%Y-%m-%d'))

class DisplayData:
    def __init__(self, connection):
        self.conn = connection
        self.cur = connection.cur

    def display_students(self):
        self.cur.execute("SELECT * FROM students")
        students = self.cur.fetchall()
        for student in students:
            print("Student data:")
            print("Student ID:", student[0])
            print("Name:", student[1])
            print("Group ID:", student[2])
            print("----------------------")

    def display_groups(self):
        self.cur.execute("SELECT * FROM groups")
        groups = self.cur.fetchall()
        for group in groups:
            print("Group data:")
            print("Group ID:", group[0])
            print("Name:", group[1])
            print("----------------------")

    def display_lecturers(self):
        self.cur.execute("SELECT * FROM lecturers")
        lecturers = self.cur.fetchall()
        for lecturer in lecturers:
            print("Lecturer data:")
            print("Lecturer ID:", lecturer[0])
            print("Name:", lecturer[1])
            print("----------------------")

    def display_subjects(self):
        self.cur.execute("SELECT * FROM subjects")
        subjects = self.cur.fetchall()
        for subject in subjects:
            print("Subject data:")
            print("Subject ID:", subject[0])
            print("Name:", subject[1])
            print("Lecturer ID:", subject[2])
            print("----------------------")

    def display_grades(self):
        self.cur.execute("SELECT * FROM grades")
        grades = self.cur.fetchall()
        for grade in grades:
            print("Grade data:")
            print("Grade ID:", grade[0])
            print("Student ID:", grade[1])
            print("Subject ID:", grade[2])
            print("Grade:", grade[3])
            print("Date:", grade[4])
            print("----------------------")

def execute_sql_query(query_file_path, parameters=None):
    with open(query_file_path, 'r') as query_file:
        query = query_file.read()

    with sqlite3.connect("university.db") as conn:
        cursor = conn.cursor()
        if parameters:
            cursor.execute(query, parameters)
        else:
            cursor.execute(query)
        result = cursor.fetchall()
        for row in result:
            print(row)
    return result

def main_with_context():
    with CreateConnection("university.db") as connection:
        create_tables = CreateTables(connection)
        create_tables.create_tables()

        insert_data = InsertData(connection)
        insert_data.insert_fake_data()

        display_data = DisplayData(connection)
        display_data.display_students()
        display_data.display_groups()
        display_data.display_lecturers()
        display_data.display_subjects()
        display_data.display_grades()

if __name__ == "__main__":
    main_with_context()
    query_result_1 = execute_sql_query("query_1.sql")
    query_result_2 = execute_sql_query("query_2.sql", parameters=("Mathematics",))
    query_result_3 = execute_sql_query("query_3.sql", parameters=("Mathematics",))
    query_result_4 = execute_sql_query("query_4.sql")
    query_result_5 = execute_sql_query("query_5.sql", parameters=("John Doe",))
    query_result_6 = execute_sql_query("query_6.sql", parameters=("Group A",))
    query_result_7 = execute_sql_query("query_7.sql", parameters=("Group A", "Mathematics"))
