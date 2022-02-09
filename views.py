from models import TrainingSite, SmsNotifier, EmailNotifier
from my_wsgi import render
from products import products


site = TrainingSite()
sms_notifier = SmsNotifier()
email_notifier = EmailNotifier()


def main_page(request):
    return '200 OK', render('index.html')


def course_list_page(request):
    return '200 OK', render('course_list.html', objects_list=site.courses)


def student_list_page(request):
    return '200 OK', render('student_list.html', objects_list=site.students)


def create_course(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        course = site.create_course('record', name)
        course.observers.append(email_notifier)
        course.observers.append(sms_notifier)
        site.courses.append(course)
        print(name)
        return '200 OK', render('create_course.html')
    else:
        return '200 OK', render('create_course.html')


def create_student(request):
    if request['method'] == 'POST':
        data = request['data']
        name = data['name']
        surname = data['surname']
        telephone = data['telephone']
        email = data['email']
        student = site.create_user('student', name, surname, telephone, email)
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
