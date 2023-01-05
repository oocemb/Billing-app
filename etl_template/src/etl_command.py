import abc
from typing import Any, Optional

from setup_logging import *

logger = get_logger()


class ETLCommand:
    """
    Абстрактный класс Команда, из экземпляров которых составляется конвейер ETL.
    Класс управляет логикой работы с данными и для непосредственной работы
    С БД вызывает экземпляры класса DataNode
    """

    @abc.abstractmethod
    def __init__(self, task, task_name, command_name):
        """
        Для инициализации Команды нужно передать
        task - словарь с параметрами команды
        task_name - общее название цепочки команд (задача)
        command_name - имя команды
        """
        self.task = task
        self.task_name = task_name
        self.command_name = command_name
        self.command_class = self.__class__.__name__

    @abc.abstractmethod
    def run(self, data=None):
        """
        Запуск команды на исполнение
        data - словарь с данными, который заполняется по мере прохождения
               задачи (цепочки команд)
        """
        pass

    @abc.abstractmethod
    def commit(self, data=None):
        """
        Подтведржеие действия команды в случае успешной операции всей цепочки
        Нужен для сохранения промежуточного состояния
        """
        pass

    @abc.abstractmethod
    def rollback(self, data=None):
        """
        Откат действия команды в случае неуспеха операции хотя бы одной команды цепочки
        Нужен для отката промежуточного состояния
        """
        pass

    def log_signature(self, prefix="", suffix=""):
        """
        Логирование с учетом данных класса
        """
        logger.info(
            f"{prefix} {self.command_class} {self.task_name} {self.command_name} {suffix}"
        )
