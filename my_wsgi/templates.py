from jinja2 import Environment, FileSystemLoader


def render(template_name, folder='templates', **kwargs):
    env = Environment()
    env.loader = FileSystemLoader(folder)
    template = env.get_template(template_name)
    return template.render(**kwargs)


if __name__ == '__main__':
    test = render('index.html', products=[{
        'category': 'Clothes',
        'title': 'Dress',
        'price': '50 $'
    }])
    print(test)
