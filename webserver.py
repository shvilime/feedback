import logging
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import urlparse, parse_qs
from settings import *
import views


class MyHandler(BaseHTTPRequestHandler):
    paths = {
        '/': {'view': 'MainTmpl', 'type': 'text/html'},
        '/comment': {'view': 'CommentTmpl', 'type': 'text/html'},
        '/view': {'view': 'ViewTmpl', 'type': 'text/html'},
        '/stat': {'view': 'StatTmpl', 'type': 'text/html'},
        '/statreg': {'view': 'StatRegTmpl', 'type': 'text/html'},
        '/view/delfeedback': {'view': 'DelFeedbackTmpl', 'type': 'text/html'},
        '/listregion': {'view': 'ListRegionTmpl', 'type': 'text/json'},
        '/listcity': {'view': 'ListCityTmpl', 'type': 'text/json'}

        # '/static/css/feedback.css': {'static': '/static/css/feedback.css', 'type': 'text/css'},
        # '/static/js/view.js': {'static': '/static/js/view.js', 'type': 'text/javascript'},
        # '/static/js/comment.js': {'static': '/static/js/comment.js', 'type': 'text/javascript'}
    }


    def _parse_path(self):
        """  Парсит полный путь запроса для выделения самого пути и параметров """
        parsed = urlparse(self.path)
        return [parsed.path, parse_qs(parsed.query)]

    def _is_view(self, path):
        """  Проверяет нахождение пути в таблице путей и тогда это темплейт """
        return path in self.paths

    def _is_static(self, path):
        """ Проверяет путь на признак статичного файла """
        return os.path.isfile(ROOT + path)

    def _get_status(self):
        """
            Проверяет пути и возвращает статус ответа сервера:
            200 - если найдет путь в таблице путей или присутствует статичный файл
            404 - если путь не найдет
        """
        status = 404
        # Получим путь без учета возможных параметров запроса
        path, params = self._parse_path()
        # Если путь есть в таблице путей (это темплейт) или если путь ведет к статичному файлу
        if self._is_view(path) or self._is_static(path):
            status = 200
        return status

    def _set_headers(self, status, content_type, value):
        """ Устанавливает заголовки ответа веб сервера """
        self.send_response(status)
        self.send_header(content_type, value)
        self.end_headers()

    def _get_content_type(self, path):
        """ Возвращает тип контента, в зависимости от запрошенных в адресе данных """
        type_content = {'.css': 'text/css',
                        '.js': 'application/javascript',
                        '.ico': 'image/x-icon',
                        '.jpg': 'image/jpeg',
                        '.png': 'image/png'}
        content_type = 'text/html'
        if path in self.paths:
            content_type = self.paths.get(path).get('type', '')
        else:
            filename, file_extension = os.path.splitext(path)
            content_type = type_content.get(file_extension, content_type)
        return content_type

    def do_GET(self):
        """ Обработка GET запроса """
        content = ''
        # Получим путь без учета возможных параметров запроса и отдельно параметры запроса
        path, params = self._parse_path()
        # Определим тип контента
        content_type = self._get_content_type(path)
        # Проверим контент на доступность и установим статус ответа сервера
        status = self._get_status()
        # Если запрашиваемый контент известен
        if status == 200:
            # Проверим, тип данных - это темплейт
            if self._is_view(path):
                # Получим class из модуля views и вызовем его для формирования контента
                view_name = self.paths.get(path).get('view', '')
                tmpl = getattr(views, view_name)()
                content = tmpl.get(params, content_type)
            # Проверим, если тип данных - это статичный файл, то просто прочитаем данные из файла
            if self._is_static(path):
                content = open(ROOT + path, 'rb').read()
        # Если контент не найден, то выведем 404 страницу
        elif status == 404:
            tmpl = getattr(views, 'View404Tmpl')()
            content = tmpl.get(params, content_type)
        # Установим заголовки и выведем контент
        self._set_headers(status, 'Content-type', content_type)
        # Если контент это строка, то переведем строку в бинарную форму
        if isinstance(content, str):
            content = bytes(content, 'UTF-8')
        self.wfile.write(content)


    def do_POST(self):
        """ Обработа POST запроса """
        content = ''
        # Получим путь без учета возможных параметров запроса
        path, params = self._parse_path()
        # Определим тип контента
        content_type = self._get_content_type(path)
        # Прочитаем длину переданного контента в запросе и сами переданные данные
        content_length = int(self.headers['Content-Length'])
        params = parse_qs(self.rfile.read(content_length).decode("UTF-8"), keep_blank_values=True)
        # Проверим контент на доступность и установим статус ответа сервера
        status = self._get_status()
        # Если запрашиваемый адрес известен
        if status == 200:
            # Проверим, тип данных - это темплейт
            if self._is_view(path):
                # Получим class из модуля views и вызовем его для передачи данных на обработку
                view_name = self.paths.get(path).get('view', '')
                tmpl = getattr(views, view_name)()
                content = tmpl.post(params)
                # Перенаправим после POST на родительский адрес
                success_url = "/" + "".join(self.path.split('/')[:-1])
                self._set_headers(302, 'Location', success_url)
        # Установим заголовки и выведем контент
        self._set_headers(status, 'Content-type', content_type)
        # Если контент это строка, то переведем строку в бинарную форму
        if isinstance(content, str):
            content = bytes(content, 'UTF-8')
        self.wfile.write(content)


def main():
    logging.basicConfig(format='%(filename)s[LINE:%(lineno)d]#%(levelname)-8s [%(asctime)s] %(message)s',
                        level=logging.INFO, filename='feedback.log')
    server_class = HTTPServer
    httpd = server_class((HOST_NAME, PORT_NUMBER), MyHandler)
    logging.info('Сервер запущен - {}:{}'.format(HOST_NAME, PORT_NUMBER))
    try:
        httpd.serve_forever()
    except KeyboardInterrupt:
        pass
    httpd.server_close()
    logging.info('Сервер остановлен - {}:{}'.format(HOST_NAME, PORT_NUMBER))


if __name__ == '__main__':
    main()
