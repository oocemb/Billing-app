import abc
from typing import Any, Optional
import json


class BaseStorage:
    @abc.abstractmethod
    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        pass

    @abc.abstractmethod
    def retrieve_state(self) -> dict:
        """Загрузить состояние локально из постоянного хранилища"""
        pass


class JsonFileStorage(BaseStorage):
    def __init__(self, file_path: Optional[str] = None):
        self.file_path = file_path

    def save_state(self, state: dict) -> None:
        """Сохранить состояние в постоянное хранилище"""
        with open(self.file_path, "w") as fp:
            json.dump(state, fp)

    def retrieve_state(self) -> dict:
        try:
            with open(self.file_path, "r") as f:
                body = f.read()
                return json.loads(body) if body else {}
        except FileNotFoundError:
            return {}


class State:
    """
    Класс для хранения состояния при работе с данными, чтобы постоянно не перечитывать данные с начала.
    Здесь представлена реализация с сохранением состояния в файл.
    В целом ничего не мешает поменять это поведение на работу с БД или распределённым хранилищем.
    """

    def __init__(self, storage: BaseStorage):
        self.storage = storage

    def set_state(self, key: str, value: Any) -> None:
        """Установить состояние для определённого ключа"""
        cur_state = self.storage.retrieve_state()
        cur_state[key] = value
        self.storage.save_state(cur_state)

    def get_state(self, key: str, default_value: str) -> Any:
        """Получить состояние по определённому ключу"""
        cur_state = self.storage.retrieve_state()
        if key in cur_state:
            return cur_state[key]
        else:
            return default_value
