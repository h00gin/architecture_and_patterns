class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if path in self.routes:
            controller = self.routes[path]
            request = {}
            for front in self.fronts:
                front(request)
            code, body = controller(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [body.encode('utf-8')]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'404 NOT FOUND']
