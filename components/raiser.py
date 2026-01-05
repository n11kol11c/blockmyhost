import os
import sys
import string
import math
import typing
import typing_extensions
import asyncio
import time
import json
import colorama
import functools

from typing import (
    Type, TypeVar,
    TypeAlias, Literal,
    Union, List, Any,
    Callable, overload
)

from colorama import Fore, Back, Style, init
colorama.init(autoreset=True)

class Raiser:
    def __init__(self, tp: str, content: str):
        self.tp = tp
        self.content = content

    @overload
    def create(self) -> None: ...

    @overload
    def create(
        self,
        *,
        color: str,
        end: Literal['-n']
    ) -> None: ...

    @overload
    def create(
        self,
        *,
        color: str,
        end: Literal['-s']
    ) -> str: ...

    def create(
        self,
        *,
        color: str = Fore.RESET,
        end: Literal['-n', '-s'] = '-n'
    ) -> str | None:
        ...
