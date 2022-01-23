import views
from my_wsgi import Application

routes = {
    '/': views.main_page,
    '/about': views.about_page
}


def products_controller(request):
    request['products'] = {
        'category': 'Shoes',
        'title': 'Boots',
        'price': '20 $'
    }


def secret_front(request):
    request['secret'] = 'some secret'


def other_front(request):
    request['key'] = 'value'


application = Application(routes, [products_controller, other_front])


# запуск:
# waitress-serve --listen=*:8000 main:application
