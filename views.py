import os, json
from urllib.request import urlopen
from database import DB
from template import HTMLFormatter
from settings import *


class AbstractView:
    """ Абстрактный класс. View.
        Аттрибуты:
        "query" - для работы с базой
        "template" - имя html файла, где хранится шаблон для вывода данных
        Методы:
        get() - обработка GET запросов веб сервера
        post() - обработка POST запросов веб сервера
        """
    template = ''
    query = ''

    def _get_template(self):
        content = ''
        if self.template:
            path = ROOT + '/html/' + self.template
            with open(path, 'r') as fh:
                content = fh.read()
        return content

    def get_data(self, params=None):
        if self.query:
            if params:
                self.query = self.query.format(*[v[0] for k, v in params.items()])
            db = DB()
            return db.execute(self.query)

    def get(self, params=None, content_type="text/html"):
        content = ""
        if content_type == "text/html":
            content = self._get_template()
            values = None
            if self.query.strip().upper().startswith('SELECT'):
                values = self.get_data(params)
            hf = HTMLFormatter()
            content = hf.format(content, rows=values)
        elif content_type == "text/json":
            values = self.get_data(params)
            content = json.dumps(values)
        return content

    def post(self, params=None):
        values = self.get_data(params)
        return "OK"


class MainTmpl(AbstractView):
    """ Просмотр основной страницы """
    template = 'index.html'


class CommentTmpl(AbstractView):
    """ Добавление комментария """
    template = 'comment.html'
    query = '''INSERT INTO feedback (firstname, lastname, middlename, email, phone, region, city, comment)
        VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')'''


class ViewTmpl(AbstractView):
    """ Просмотр списка отзывов """
    template = 'view.html'
    query = '''select f.id, f.lastname || ' ' || f.firstname || ' ' || IFNULL(f.middlename,'') as user,
               IFNULL(f.email,''), IFNULL(f.phone,''), IFNULL(r.name,'') as region, IFNULL(c.name,'') as city, f.comment
               from feedback f left join city c on (f.city = c.id) left join region r on (f.region = r.id)'''


class DelFeedbackTmpl(AbstractView):
    """ Удаление отзыва """
    query = '''DELETE FROM feedback WHERE id = {};'''


class StatTmpl(AbstractView):
    """ Просмотр статистики отзывов по регионам """
    template = 'stat.html'
    query = '''select * from (select r.id, r.name, count(f.id) as col from region r 
               left outer join feedback f on r.id = f.region
               group by r.name)
               where col>=1'''


class StatRegTmpl(AbstractView):
    """ Просмотр статистики в разрезе одного региона """
    template = 'statreg.html'
    query = '''select * from (select c.region, c.name, count(f.id) as col from city c 
               left outer join feedback f on c.id = f.city
               group by c.name)
               where col>0 and region='{}' '''


class ListRegionTmpl(AbstractView):
    """ Выбрать список регионов для поля формы """
    query = '''select * from region'''


class ListCityTmpl(AbstractView):
    """ Выбрать список городов региона для поля формы """
    query = '''select * from city 
               where region='{}' '''
