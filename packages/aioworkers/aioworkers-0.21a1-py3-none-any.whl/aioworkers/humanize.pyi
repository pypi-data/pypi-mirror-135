from typing import Any, Union

def size(value: int, suffixes: list = ...) -> str: ...

pattern_valid: Any
pattern: Any
size_levels: Any

def parse_size(value: Union[int, float, str]) -> Union[int, float]: ...

durations: Any

def parse_duration(value: Union[int, float, str]) -> Union[int, float]: ...
