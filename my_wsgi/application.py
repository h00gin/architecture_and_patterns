class Application:
    def __init__(self, routes, fronts):
        self.routes = routes
        self.fronts = fronts

    def parse_input_data(self, data: str):
        dict_result = {}
        if data:
            params = data.split('&')
            for item in params:
                key, value = item.split('=')
                dict_result[key] = value
        return dict_result

    def get_wsgi_input_data(self, environ) -> bytes:
        content_length_data = environ.get('CONTENT_LENGTH')
        content_length = int(content_length_data) if content_length_data else 0
        data = environ['wsgi.input'].read(content_length) if content_length > 0 else b''
        return data

    def parse_wsgi_input_data(self, data: bytes) -> dict:
        dict_result = {}
        if data:
            data_str = data.decode(encoding='utf-8')
            dict_result = self.parse_input_data(data_str)
        return dict_result

    def __call__(self, environ, start_response):
        path = environ['PATH_INFO']

        if path[-1] != '/':
            path = f'{path}/'

        method = environ['REQUEST_METHOD']
        data = self.get_wsgi_input_data(environ)
        data = self.parse_wsgi_input_data(data)

        query_string = environ['QUERY_STRING']
        request_params = self.parse_input_data(query_string)

        if path in self.routes:
            controller = self.routes[path]
            request = {}
            request['method'] = method
            request['data'] = data
            request['request_params'] = request_params

            for front in self.fronts:
                front(request)
            code, body = controller(request)
            start_response(code, [('Content-Type', 'text/html')])
            return [body.encode('utf-8')]
        else:
            start_response('404 NOT FOUND', [('Content-Type', 'text/html')])
            return [b'404 NOT FOUND']


class DebugApplication(Application):
    def __init__(self, routes, fronts):
        self.application = Application(routes, fronts)
        super().__init__(routes, fronts)

    def __call__(self, environ, start_response):
        print('Debug')
        print(environ)
        return self.application(environ, start_response)


class FakeApplication(Application):
    def __init__(self, routes, fronts):
        self.application = Application(routes, fronts)
        super().__init__(routes, fronts)

    def __call__(self, environ, start_response):
        start_response('200 OK', [('Content-Type', 'text/html')])
        return [b'Hello from FAKE!']
