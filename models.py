from patterns.observer import Subject, Observer
from patterns.prototype import PrototypeMixin


class User:
    def __init__(self, name, surname, telephone, email):
        self.name = name
        self.surname = surname
        self.telephone = telephone
        self.email = email


class Teacher(User):
    pass


class Student(User):

    def __init__(self, name, surname, telephone, email):
        self.courses = []
        super().__init__(name, surname, telephone, email)


class SimpleFactory:

    def __init__(self, types=None):
        self.types = types or {}


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, name, surname, telephone, email):
        return cls.types[type_](name, surname, telephone, email)


class Course(PrototypeMixin, Subject):

    def __init__(self, name):
        self.name = name
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        self.notify()


class InteractiveCourse(Course):
    pass


class RecordCourse(Course):
    pass


class CourseFactory:
    types = {
        'interactive': InteractiveCourse,
        'record': RecordCourse
    }

    @classmethod
    def create(cls, type_, name):
        return cls.types[type_](name)


class TrainingSite:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []

    def create_user(self, type_, name, surname, telephone, email):
        return UserFactory.create(type_, name, surname, telephone, email)

    def create_course(self, type_, name):
        return CourseFactory.create(type_, name)

    def get_course(self, name) -> Course:
        for item in self.courses:
            if item.name == name:
                return item
        return None

    def get_student(self, name) -> Student:
        for item in self.students:
            if item.name == name:
                return item
        return None


class SmsNotifier(Observer):

    def update(self, subject: Course):
        print(f'SMS notification - student signed up for the course: {subject.students[-1].name}')


class EmailNotifier(Observer):

    def update(self, subject: Course):
        print(f'Email notification - student signed up for the course: {subject.students[-1].name}')
