from my_wsgi import render
from products import products


def main_page(request):
    return '200 OK', render('index.html', products=products)


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
