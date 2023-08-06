from typing import Any

class HttpException(Exception):
    status: Any
    def __init__(self, status: int = ...) -> None: ...
