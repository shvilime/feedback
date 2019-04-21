"""
Settings for Feedback project.
"""

import os

# Адрес носта на котором запускается сервер и номер порта
HOST_NAME = 'localhost'
PORT_NUMBER = 8080

# Полный путь к местоположения сервиса
ROOT = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'feedback')

# Версия сервиса
VERSION = "0.0.1"


# Минимальное количество отзывов по региону для включения в статистику
STAT_LIMIT = 1