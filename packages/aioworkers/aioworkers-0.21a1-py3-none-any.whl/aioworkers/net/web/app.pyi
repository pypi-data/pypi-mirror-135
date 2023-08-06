from .request import Request as Request
from aioworkers.core.base import LoggingEntity as LoggingEntity
from aioworkers.net.web.exceptions import HttpException as HttpException
from typing import Any, Awaitable, Callable, Iterable, Mapping, NamedTuple

class Route(NamedTuple):
    handler: Any
    kwargs: Any

class Application(LoggingEntity):
    async def init(self) -> None: ...
    def add_route(self, method, path, handler, name: Any | None = ..., **kwargs) -> None: ...
    async def __call__(self, scope: Mapping, receive: Callable[[], Awaitable], send: Callable[[Mapping], Awaitable]): ...

class Resources(Iterable):
    def __init__(self, resources: Mapping) -> None: ...
    def __iter__(self): ...
