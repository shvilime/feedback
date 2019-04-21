import json, logging
from database import DB
from template import HTMLFormatter
from settings import *


class BaseView:
    """
        Базовый класс. View.
        Аттрибуты:
        "query_get" - запрос на получение данных для работы с базой
        "query_post" - запрос на добавление/изменение данных для работы с базой
        "template" - имя html файла, где хранится шаблон для вывода данных
        Методы:
        get() - обработка GET запросов веб сервера
        post() - обработка POST запросов веб сервера
    """
    template = ''
    query_get = ''
    query_post = ''

    def _get_template(self):
        """ Считывает шаблон из html файла для вывода """
        content = ''
        if self.template:
            path = ROOT + '/html/' + self.template
            try:
                with open(path, 'r') as fh:
                    content = fh.read()
            except IOError:
                logging.error('Ошибка при чтении темплейта - {}'.format(path))
        return content

    def _process_query(self, query='', params=None):
        """
            Заполняет запрос к базе параметрами и передает DB на исполнение
            возвращает список строк-кортежей
        """
        data = []
        if query:
            db = DB()
            if params:
                query = query.format(*[v[0] for k, v in params.items()])
            data = db.execute(query)
        return data

    def get(self, params=None, content_type="text/html"):
        """ Формирует контент для web сервера по запросу GET """
        content = ""
        data = self._process_query(self.query_get, params)
        if content_type == "text/html":
            # Создадим объект для форматирования html
            hf = HTMLFormatter()
            try:
                content = hf.format(self._get_template(), rows=data)
            except:
                logging.error('Ошибка обработки шаблона {}'.format(self.template))
        elif content_type == "text/json":
            content = json.dumps(data)
        return content

    def post(self, params=None):
        """ Формирует контент для web сервера по запросу POST """
        self._process_query(self.query_post, params)
        return "OK"


class MainTmpl(BaseView):
    """ Просмотр основной страницы """
    template = 'index.html'


class View404Tmpl(BaseView):
    """ Просмотр 404 страницы """
    template = '404.html'


class CommentTmpl(BaseView):
    """ Добавление комментария """
    template = 'comment.html'
    query_post = '''INSERT INTO feedback (firstname, lastname, middlename, email, phone, region, city, comment)
                    VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')'''


class ViewTmpl(BaseView):
    """ Просмотр списка отзывов """
    template = 'view.html'
    query_get = '''SELECT f.id, f.lastname || ' ' || f.firstname || ' ' || f.middlename AS USER,
                   f.email, f.phone, IFNULL(r.name,'') AS region, IFNULL(c.name,'') AS city, f.comment
                   FROM feedback f LEFT JOIN city c ON (f.city = c.id) LEFT JOIN region r ON (f.region = r.id)'''


class DelFeedbackTmpl(BaseView):
    """ Удаление отзыва """
    query_post = '''DELETE FROM feedback WHERE id = {}'''


class StatTmpl(BaseView):
    """ Просмотр статистики отзывов по регионам """
    template = 'stat.html'
    query_get = '''SELECT r.id, r.name, COUNT(f.id) AS col FROM region r 
                   LEFT OUTER JOIN feedback f ON r.id = f.region
                   GROUP BY r.id
                   HAVING col >={}'''.format(STAT_LIMIT)


class StatRegTmpl(BaseView):
    """ Просмотр статистики в разрезе одного региона """
    template = 'statreg.html'
    query_get = '''SELECT f.region, c.name, COUNT(f.id) AS col FROM city c 
                   LEFT OUTER JOIN feedback f ON c.id = f.city
                   WHERE f.region={}
                   GROUP BY c.id
                   HAVING col>0'''


class ListRegionTmpl(BaseView):
    """ Выбрать список регионов для поля формы """
    query_get = '''SELECT * FROM region'''


class ListCityTmpl(BaseView):
    """ Выбрать список городов региона для поля формы """
    query_get = '''SELECT * FROM city 
                   WHERE region={} '''
