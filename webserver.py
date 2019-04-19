import time, os, sys
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from urllib.request import urlopen
import views

HOST_NAME = 'localhost'
PORT_NUMBER = 8080
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'feedback')


class MyServer(BaseHTTPRequestHandler):
    paths = {
        '/': {'view': 'main_tmpl', 'type': 'text/html'},
        '/comment': {'view': 'comment_tmpl', 'type': 'text/html'},
        '/view': {'view': 'view_tmpl', 'type': 'text/html'},
        '/stat': {'view': 'stat_tmpl', 'type': 'text/html'},
        '/statreg': {'view': 'statreg_tmpl', 'type': 'text/html'},
        '/view/delfeedback': {'view': 'delfeedback_tmpl', 'type': 'text/html'},
        '/listregion': {'view': 'listregion_tmpl', 'type': 'text/json'},
        '/listcity': {'view': 'listcity_tmpl', 'type': 'text/json'},
        '/js/view.js': {'static': '/js/view.js', 'type': 'text/javascript'},
        '/js/comment.js': {'static': '/js/comment.js', 'type': 'text/javascript'}

    }

    _content_type = 'text/html'
    _status = 200

    def _check_path(self):
        # Проверяет пути и устанавливает статус
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
        if self._status == 200:
            # Получим class из модуля views и вызовем их для формирования темплейта
            viewname = self.paths.get(self.path).get('view', '')
            if viewname:
                tmpl = getattr(views, viewname)()
                content = tmpl.get(self.parameters)
            static_file = self.paths.get(self.path).get('static', '')
            if static_file:
                content = open(ROOT + static_file, 'r').read()
        self.wfile.write(bytes(content, 'UTF-8'))

    def do_POST(self):
        content = ''
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length).decode("UTF-8")
        self._check_path()
        self._set_headers()
        if self._status == 200:
            # Получим class из модуля views и вызовем их для формирования темплейта
            viewname = self.paths.get(self.path).get('view', '')
            if viewname:
                tmpl = getattr(views, viewname)()
                self.parameters = parse_qs(post_data, keep_blank_values=True)
                content = tmpl.post(self.parameters)
                # success_url = "/".join(self.path.split('/')[:-1])
                # urlopen('http://localhost:8080'+success_url)
                # Здесь я нихочу ничего возвращать !!! хочу уйти на другую страницу.
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
