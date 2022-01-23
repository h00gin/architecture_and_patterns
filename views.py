from my_wsgi import render
from products import products


def main_page(request):
    return '200 OK', render('index.html', products=products)


def about_page(request):
    secret = request.get('secret', None)
    return '200 OK', render('about.html', secret=secret)

