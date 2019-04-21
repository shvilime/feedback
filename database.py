import os, sqlite3, logging


class DB(object):
    """ Объект для инициализации базы SQLite3  и выполнения операций с ней """

    def __db_initial__(self):
        """ Первоначальная инициализация файла базы данных если база не найдена """
        if not os.path.isfile(self.database):
            # Прочтем скрипт первоначального создания базы из файла
            query = open('feedback.sql', 'r').read()
            # Проверим скрипт на завершенность, на всякий случай
            if sqlite3.complete_statement(query):
                # Соединимся с базой данных, получим курсур и выполним скрипт.
                self.connect()
                try:
                    self.cursor.executescript(query)
                except sqlite3.Error as e:
                    logging.critical('Ошибка первичной инициализации базы:', e.args[0])
                else:
                    self.close()

    def __init__(self, database='feedback.sqlite'):
        """ Инициализация объекта """
        self.connected = False
        self.database = database
        self.__db_initial__()

    def connect(self):
        """ Подключение к базе SQLite3 """
        if not self.connected:
            try:
                self.connection = sqlite3.connect(self.database)
                self.cursor = self.connection.cursor()
                self.connected = True
            except sqlite3.Error as e:
                logging.error("Ошибка соединения с базой!")

    def close(self):
        """ Закрыть базу SQLite3 """
        self.connection.commit()
        self.connection.close()
        self.connected = False

    def execute(self, statement, limit=None):
        """  Выполняет SQL выражения """
        if not self.connected:
            self.connect()
        try:
            self.cursor.execute(statement)
            if statement.strip().upper().startswith('SELECT'):
                rows = self.cursor.fetchall()
                return rows[len(rows) - limit if limit else 0:]
        except sqlite3.Error as e:
            logging.error('Произошла ошибка: {}'.format(e.args[0]))
            logging.error('При выполнении выражения: {}'.format(statement))
        else:
            self.connection.commit()
