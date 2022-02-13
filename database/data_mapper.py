import abc
import sqlite3

from models import Student, Course, Category


class RecordNotFoundException(Exception):
    def __init__(self, message):
        super().__init__(f'Record not found: {message}')


class DbCommitException(Exception):
    def __init__(self, message):
        super().__init__(f'Db commit error: {message}')


class DbUpdateException(Exception):
    def __init__(self, message):
        super().__init__(f'Db update error: {message}')


class DbDeleteException(Exception):
    def __init__(self, message):
        super().__init__(f'Db delete error: {message}')

#
# class StudentMapper(metaclass=abc.ABC):
#     @abc.abstractmethod
#     def find_by_id(self, id_student):
#         pass


class SqliteStudentMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def find_by_id(self, id_student):
        statement = f'SELECT ID, NAME, SURNAME, TELEPHONE, EMAIL FROM STUDENTS WHERE ID=?'
        self.cursor.execute(statement, (id_student,))
        result = self.cursor.fetchone()
        if result:
            return Student(*result)
        else:
            raise RecordNotFoundException(f'record with id={id_student} not found')

    def insert(self, student):
        statement = f'INSERT INTO STUDENTS (NAME, SURNAME, TELEPHONE, EMAIL) VALUES (?, ?, ?, ?)'
        self.cursor.execute(statement, (student.name, student.surname, student.telephone, student.email))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, student):
        statement = f'UPDATE STUDENTS SET NAME=?, SURNAME=?, TELEPHONE=?, EMAIL=? WHERE ID=?'
        self.cursor.execute(statement, (student.name, student.surname, student.telephone, student.email, student.id))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, student):
        statement = f'DELETE FROM STUDENTS WHERE ID=?'
        self.cursor.execute(statement, (student.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class SqliteCategoryMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def find_by_id(self, id_category):
        statement = f'SELECT ID, NAME FROM CATEGORIES WHERE ID=?'
        self.cursor.execute(statement, (id_category,))
        result = self.cursor.fetchone()
        if result:
            return Category(*result)
        else:
            raise RecordNotFoundException(f'record with id={id_category} not found')

    def insert(self, category):
        statement = f'INSERT INTO CATEGORIES (NAME) VALUES (?)'
        self.cursor.execute(statement, (category.name, ))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, category):
        statement = f'UPDATE CATEGORIES SET NAME=? WHERE ID=?'
        self.cursor.execute(statement, (category.name,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, category):
        statement = f'DELETE FROM CATEGORIES WHERE ID=?'
        self.cursor.execute(statement, (category.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


class SqliteCourseMapper:
    def __init__(self, connection):
        self.connection = connection
        self.cursor = connection.cursor()

    def find_by_id(self, id_course):
        statement = f'SELECT ID, NAME, CATEGORY_ID FROM COURSES WHERE ID=?'
        self.cursor.execute(statement, (id_course,))
        result = self.cursor.fetchone()
        if result:
            return Course(*result)
        else:
            raise RecordNotFoundException(f'record with id={id_course} not found')

    def insert(self, course):
        statement = f'INSERT INTO COURSES (NAME, CATEGORY_ID) VALUES (?, ?)'
        self.cursor.execute(statement, (course.name, course.category))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbCommitException(e.args)

    def update(self, course):
        statement = f'UPDATE COURSES SET NAME=? CATEGORY_ID=? WHERE ID=?'
        self.cursor.execute(statement, (course.name, course.category))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbUpdateException(e.args)

    def delete(self, course):
        statement = f'DELETE FROM COURSES WHERE ID=?'
        self.cursor.execute(statement, (course.id,))
        try:
            self.connection.commit()
        except Exception as e:
            raise DbDeleteException(e.args)


connection = sqlite3.connect('patterns.sqlite')
student_mapper = SqliteStudentMapper(connection)
student_1 = student_mapper.find_by_id(2)
print(student_1.__dict__)

category_mapper = SqliteCategoryMapper(connection)
category_1 = category_mapper.find_by_id(3)
print(category_1.__dict__)

course_mapper = SqliteCourseMapper(connection)
course_1 = course_mapper.find_by_id(1)
print(course_1.__dict__)
