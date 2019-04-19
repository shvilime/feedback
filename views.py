import os, json
from urllib.request import urlopen
from database import DB
from template import HTMLFormatter
from webserver import ROOT


class abstract_view():
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

    def get(self, params=None):
        content = self._get_template()
        values = None
        if self.query.strip().upper().startswith('SELECT'):
            values = self.get_data(params)
        hf = HTMLFormatter()
        return hf.format(content, rows=values)

    def post(self, params=None):
        values = self.get_data(params)
        return json.dumps(values)


# ********************************************************************************

class main_tmpl(abstract_view):
    """ Просмотр основной страницы """
    template = 'index.html'


# ********************************************************************************

class comment_tmpl(abstract_view):
    """ Добавление комментария """
    template = 'comment.html'
    query = '''INSERT INTO feedback (firstname, lastname, middlename, email, phone, region, city, comment)
        VALUES ('{}','{}','{}','{}','{}','{}','{}','{}')'''


# ********************************************************************************

class view_tmpl(abstract_view):
    """ Просмотр списка отзывов """
    template = 'view.html'
    query = '''select f.id, f.lastname || ' ' || f.firstname || ' ' || IFNULL(f.middlename,'') as user,
               IFNULL(f.email,''), IFNULL(f.phone,''), IFNULL(r.name,'') as region, IFNULL(c.name,'') as city, f.comment
               from feedback f left join city c on (f.city = c.id) left join region r on (f.region = r.id)'''


# ********************************************************************************

class delfeedback_tmpl(abstract_view):
    """ Удаление отзыва """
    query = '''DELETE FROM feedback WHERE id = {};'''


# ********************************************************************************

class stat_tmpl(abstract_view):
    """ Просмотр статистики отзывов по регионам """
    template = 'stat.html'
    query = '''select * from (select r.id, r.name, count(f.id) as col from region r 
               left outer join feedback f on r.id = f.region
               group by r.name)
               where col>=1'''


# ********************************************************************************

class statreg_tmpl(abstract_view):
    """ Просмотр статистики в разрезе одного региона """
    template = 'statreg.html'
    query = '''select * from (select c.region, c.name, count(f.id) as col from city c 
               left outer join feedback f on c.id = f.city
               group by c.name)
               where col>0 and region='{}' '''


# ********************************************************************************

class listregion_tmpl(abstract_view):
    """ Выбрать список регионов для поля формы """
    query = '''select * from region'''

# ********************************************************************************

class listcity_tmpl(abstract_view):
    """ Выбрать список городов региона для поля формы """
    query = '''select * from city 
               where region='{}' '''