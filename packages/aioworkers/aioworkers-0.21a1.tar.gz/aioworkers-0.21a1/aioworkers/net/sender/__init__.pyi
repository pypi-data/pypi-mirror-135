import abc
from abc import abstractmethod
from aioworkers.core.base import AbstractEntity as AbstractEntity

class AbstractSender(AbstractEntity, metaclass=abc.ABCMeta):
    @abstractmethod
    async def send_message(self, msg): ...
    async def send(self, *args, **kwargs) -> None: ...
