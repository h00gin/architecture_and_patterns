import sqlite3

from database.data_mapper_and_unit_of_work import SqliteStudentMapper
from models import Student

connection = sqlite3.connect('patterns.sqlite')


class MapperRegistry:
    @staticmethod
    def get_mapper(obj):
        if isinstance(obj, Student):
            return SqliteStudentMapper(connection, Student)
