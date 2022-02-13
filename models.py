from patterns.observer import Subject, Observer
from patterns.prototype import PrototypeMixin


class User:
    def __init__(self, id, name, surname, telephone, email):
        self.id = id
        self.name = name
        self.surname = surname
        self.telephone = telephone
        self.email = email


class Teacher(User):
    pass


class Student(User, Subject):

    def __init__(self, id, name, surname, telephone, email):
        self.courses = []
        self.notify()
        super().__init__(id, name, surname, telephone, email)


class SimpleFactory:

    def __init__(self, types=None):
        self.types = types or {}


class UserFactory:
    types = {
        'student': Student,
        'teacher': Teacher
    }

    @classmethod
    def create(cls, type_, id, name, surname, telephone, email):
        return cls.types[type_](id, name, surname, telephone, email)


class Category:
    auto_id = 0

    def __getitem__(self, item):
        return self.courses[item]

    def __init__(self, name, category):
        self.id = Category.auto_id
        Category.auto_id += 1
        self.name = name
        self.category = category
        self.courses = []

    def course_count(self):
        result = len(self.courses)
        if self.category:
            result += self.category.course_count()
        return result


class Course(PrototypeMixin, Subject):

    def __init__(self, id, name, category):
        self.id = id
        self.name = name
        self.category = category
        self.category.courses.append(self)
        self.students = []
        super().__init__()

    def __getitem__(self, item):
        return self.students[item]

    def add_student(self, student: Student):
        self.students.append(student)
        student.courses.append(self)
        # self.notify()


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
    def create(cls, type_, id, name, category):
        return cls.types[type_](id, name, category)


class TrainingSite:
    def __init__(self):
        self.teachers = []
        self.students = []
        self.courses = []
        self.categories = []

    def create_user(self, type_, id, name, surname, telephone, email):
        return UserFactory.create(type_, id, name, surname, telephone, email)

    def create_category(self, name, category=None):
        return Category(name, category)

    def find_category_by_id(self, id):
        for item in self.categories:
            if item.id == id:
                return item
        raise Exception(f'Нет категории курсов с данным id: {id}')

    def create_course(self, type_, id, name, category):
        return CourseFactory.create(type_, id, name, category)

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
