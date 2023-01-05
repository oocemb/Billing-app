import abc


class DataNode:
    """
    Абстрактный класс для работы с базами данных.
    """

    @abc.abstractmethod
    def __init__(self, settings):
        pass

    @abc.abstractmethod
    def connect(self):
        """Инициализация подключения"""
        pass

    @abc.abstractmethod
    def pull(self, query):
        """Запрос к базе  данных"""
        pass

    @abc.abstractmethod
    def push(self, data):
        """Отправка данных в базу"""
        pass
