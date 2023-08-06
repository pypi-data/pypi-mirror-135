import argparse
from . import utils as utils
from .core import command as command
from .core.config import Config as Config
from .core.context import Context as Context, GroupResolver as GroupResolver
from .core.plugin import Plugin as Plugin, search_plugins as search_plugins
from typing import Any

parser: Any
group: Any
PROMPT: str

class PidFileType(argparse.FileType):
    def __call__(self, string): ...

context: Any

def main(*config_files, args: Any | None = ..., config_dirs=..., commands=..., config_dict: Any | None = ...): ...
def process_iter(cfg, cpus=...): ...
def create_process(cfg): ...
def loop_run(conf: Any | None = ..., future: Any | None = ..., group_resolver: Any | None = ..., ns: Any | None = ..., cmds: Any | None = ..., argv: Any | None = ..., loop: Any | None = ..., prompt: Any | None = ..., process_name: Any | None = ...): ...

class UriType(argparse.FileType):
    def __call__(self, string): ...

class ExtendAction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string: Any | None = ...) -> None: ...

class plugin(Plugin):
    def add_arguments(self, parser) -> None: ...

def main_with_conf(*args, **kwargs) -> None: ...
