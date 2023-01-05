from abc import ABC, abstractmethod


class Validator(ABC):
    @staticmethod
    @abstractmethod
    async def validate(**kwargs) -> bool:
        pass
