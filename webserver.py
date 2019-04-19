import time, os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
from settings import *
import views


class MyServer(BaseHTTPRequestHandler):
    paths = {
        '/': {'view': 'MainTmpl', 'type': 'text/html'},
        '/comment': {'view': 'CommentTmpl', 'type': 'text/html'},
        '/view': {'view': 'ViewTmpl', 'type': 'text/html'},
        '/stat': {'view': 'StatTmpl', 'type': 'text/html'},
        '/statreg': {'view': 'StatRegTmpl', 'type': 'text/html'},
        '/view/delfeedback': {'view': 'DelFeedbackTmpl', 'type': 'text/html'},
        '/listregion': {'view': 'ListRegionTmpl', 'type': 'text/json'},
        '/listcity': {'view': 'ListCityTmpl', 'type': 'text/json'},
        '/js/view.js': {'static': '/js/view.js', 'type': 'text/javascript'},
        '/js/comment.js': {'static': '/js/comment.js', 'type': 'text/javascript'}

    }

    _content_type = 'text/html'
    _status = 200

    def _check_path(self):
        # Проверяет пути и устанавливает статус ответа
        self.parameters = parse_qs(urlparse(self.path).query)
        self.path = urlparse(self.path).path
        if self.path in self.paths:
            self._status = 200
            self._content_type = self.paths.get(self.path).get('type', '')
        else:
            self._status = 500

    def _set_headers(self):
        # Устанавливает заголовки ответа
        self.send_response(self._status)
        self.send_header('Content-type', self._content_type)
        self.end_headers()

    def do_GET(self):
        content = ''
        self._check_path()
        self._set_headers()
        if self._status == 200:     # Если запрашиваемый адрес известен
            # Проверим, тип данных - это темплейт
            viewname = self.paths.get(self.path).get('view', '')
            if viewname:
                # Получим class из модуля views и вызовем его для формирования контента
                tmpl = getattr(views, viewname)()
                content = tmpl.get(self.parameters)
            # Проверим, тип данных - это статичный файл
            static_file = self.paths.get(self.path).get('static', '')
            if static_file:
                # Просто прочитаем данные из файла
                content = open(ROOT + static_file, 'r').read()
        self.wfile.write(bytes(content, 'UTF-8'))

    def do_POST(self):
        content = ''
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("UTF-8")
        self._check_path()
        self._set_headers()
        if self._status == 200:     # Если запрашиваемый адрес известен
            # Проверим, тип данных - это известный темплейт
            viewname = self.paths.get(self.path).get('view', '')
            if viewname:
                # Получим class из модуля views и вызовем его для формирования темплейта
                tmpl = getattr(views, viewname)()
                self.parameters = parse_qs(post_data, keep_blank_values=True)
                content = tmpl.post(self.parameters)
                # success_url = "/".join(self.path.split('/')[:-1])
                # urlopen('http://localhost:8080'+success_url)
                # Здесь я нe хочу ничего возвращать !!! хочу уйти на другую страницу.
        self.wfile.write(bytes(content, 'UTF-8'))


def main():
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyServer)
    print(time.asctime(), 'Server Starts - %s:%s' % (HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    print(time.asctime(), 'Server Stops - %s:%s' % (HOST_NAME, PORT_NUMBER))


if __name__ == '__main__':
    main()
