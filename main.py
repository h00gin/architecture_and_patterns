import views

from my_wsgi import Application
from my_wsgi.application import DebugApplication, FakeApplication
from products import products


routes = {
    '/': views.main_page,
    '/create_category/': views.about_page,
    '/category_list/': views.about_page,
    '/create_course/': views.create_course,
    '/course_list/': views.course_list_page,
    '/copy_course/': views.copy_course,
    '/create_student/': views.create_student,
    '/student_list/': views.student_list_page,
    '/add_student/': views.add_student_by_course,
    '/products/': views.products_page,
    '/about/': views.about_page,
    '/contacts/': views.contacts_view
}


def products_controller(request):
    request['products'] = products


def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'value'


application = Application(routes, [products_controller, other_front])
# application = DebugApplication(routes, [products_controller, other_front])
# application = FakeApplication(routes, [products_controller, other_front])


# запуск:
# waitress-serve --listen=*:8000 main:application
