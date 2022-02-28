import abc
import sqlite3
import threading

from database.mapper_registry import MapperRegistry
from models import Student, Course, Category

connection = sqlite3.connect('patterns.sqlite')


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


class SqliteStudentMapper:
    def __init__(self, connection, cls):
        self.connection = connection
        self.cursor = connection.cursor()
        self.cls = cls

    def find_by_id(self, id_student):
        statement = f'SELECT ID, NAME, SURNAME, TELEPHONE, EMAIL FROM STUDENTS WHERE ID=?'
        self.cursor.execute(statement, (id_student,))
        result = self.cursor.fetchone()
        if result:
            return self.cls(*result)
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
    def __init__(self, connection, cls):
        self.connection = connection
        self.cursor = connection.cursor()
        self.cls = cls

    def find_by_id(self, id_category):
        statement = f'SELECT ID, NAME FROM CATEGORIES WHERE ID=?'
        self.cursor.execute(statement, (id_category,))
        result = self.cursor.fetchone()
        if result:
            return self.cls(*result)
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
    def __init__(self, connection, cls):
        self.connection = connection
        self.cursor = connection.cursor()
        self.cls = cls

    def find_by_id(self, id_course):
        statement = f'SELECT ID, NAME, CATEGORY_ID FROM COURSES WHERE ID=?'
        self.cursor.execute(statement, (id_course,))
        result = self.cursor.fetchone()
        if result:
            return self.cls(*result)
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


class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return SqliteStudentMapper(connection)


class UnitOfWork:
    current = threading.local

    def __init__(self):
        self.new_objects = []
        self.dirty_objects = []
        self.removed_objects = []

    def register_new(self, obj):
        self.new_objects.append(obj)

    def register_dirty(self, obj):
        self.dirty_objects.append(obj)

    def register_removed(self, obj):
        self.removed_objects.append(obj)

    def commit(self):
        self.insert_new()
        self.update_dirty()
        self.delete_removed()

    def insert_new(self):
        for obj in self.new_objects:
            MapperRegistry.get_mapper(obj).insert(obj)

    def update_dirty(self):
        for obj in self.dirty_objects:
            MapperRegistry.get_mapper(obj).update(obj)

    def delete_removed(self):
        for obj in self.removed_objects:
            MapperRegistry.get_mapper(obj).delete(obj)

    @staticmethod
    def new_current():
        __class__.set_current(UnitOfWork())

    @classmethod
    def set_current(cls, unit_of_work):
        cls.current.unit_of_work = unit_of_work

    @classmethod
    def get_current(cls):
        return cls.current.unit_of_work


class DomainObject(metaclass=abc.ABC):
    def mark_new(self):
        UnitOfWork.get_current().register_new(self)

    def mark_dirty(self):
        UnitOfWork.get_current().register_dirty(self)

    def mark_removed(self):
        UnitOfWork.get_current().register_removed(self)


try:
    UnitOfWork.new_current()
    new_student_1 = Student(None, 'Igor', 'Igorev', '808888', '4@gmail.com')
    new_student_1.mark_new()

    new_student_2 = Student(None, 'Fedor', 'Fedorov', '848488', '5@gmail.com')
    new_student_2.mark_new()

    student_mapper = SqliteStudentMapper(connection)
    exists_student_1 = student_mapper.find_by_id(1)
    exists_student_1.mark_dirty()
    print(exists_student_1.name)
    exists_student_1.name += ' Senior'
    print(exists_student_1.name)

    exists_student_2 = student_mapper.find_by_id(2)
    exists_student_2.mark_removed()

    print(UnitOfWork.get_current().__dict__)

    UnitOfWork.get_current().commit()
except Exception as e:
    print(e.args)

finally:
    UnitOfWork.get_current(None)

print(UnitOfWork.get_current())


category_mapper = SqliteCategoryMapper(connection)
category_1 = category_mapper.find_by_id(3)
print(category_1.__dict__)

course_mapper = SqliteCourseMapper(connection)
course_1 = course_mapper.find_by_id(1)
print(course_1.__dict__)
