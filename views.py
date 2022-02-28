from models import TrainingSite
from my_wsgi import render
from products import products


site = TrainingSite()
# sms_notifier = SmsNotifier()
# email_notifier = EmailNotifier()


def main_page(request):
    return '200 OK', render('index.html')


def course_list_page(request):
    return '200 OK', render('course_list.html', objects_list=site.courses)


def student_list_page(request):
    return '200 OK', render('student_list.html', objects_list=site.students)


def category_list(request):
    return '200 OK', render('category_list.html', objects_list=site.categories)


def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        id = None
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
            course = site.create_course('record', id, name, category)
            site.courses.append(course)
        return '200 OK', render('create_course.html')
    else:
        categories = site.categories
        return '200 OK', render('create_course.html', categories=categories)


def change_course(request):
    if request['method'] == 'POST':
        data = request['data']
        course_name = data['course_name']
        course = site.get_course(course_name)
        new_name = data['new_name']
        course.change_course(new_name)
    return '200 OK', render('change_course.html', courses=site.courses)


def create_category(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        category_id = data.get('category_id')
        category = None
        if category_id:
            category = site.find_category_by_id(int(category_id))
        new_category = site.create_category(name, category)
        site.categories.append(new_category)
        return '200 OK', render('create_category.html')
    else:
        categories = site.categories
        return '200 OK', render('create_category.html', categories=categories)


def create_student(request):
    if request['method'] == 'POST':
        data = request['data']
        id = None
        name = data['name']
        surname = data['surname']
        telephone = data['telephone']
        email = data['email']
        student = site.create_user('student', id, name, surname, telephone, email)
        site.students.append(student)
        return '200 OK', render('create_student.html')
    else:
        return '200 OK', render('create_student.html')


def add_student_by_course(request):
    if request['method'] == 'POST':
        data = request['data']
        course_name = data['course_name']
        course = site.get_course(course_name)
        student_name = data['student_name']
        student = site.get_student(student_name)
        course.add_student(student)
        # student.update(course)
    return '200 OK', render('add_student.html', courses=site.courses, students=site.students)


def copy_course(request):
    request_params = request['request_params']
    name = request_params['name']
    old_course = site.get_course(name)
    if old_course:
        new_name = f'copy_{name}'
        new_course = old_course.clone()
        new_course.name = new_name
        site.courses.append(new_course)
    return '200 OK', render('course_list.html', objects_list=site.courses)


def products_page(request):
    return '200 OK', render('products.html', products=products)


def about_page(request):
    secret = request.get('secret', None)
    return '200 OK', render('about.html', secret=secret)


def contacts_view(request):
    if request['method'] == 'POST':
        data = request['data']
        title = data['title']
        email = data['email']
        text = data['text']
        print(f'Пришло сообщение от: {email}\nтема сообщения: {title}\nтекст сообщения: {text}')
        return '200 OK', render('contacts.html')
    else:
        return '200 OK', render('contacts.html')
