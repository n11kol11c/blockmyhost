import colorama
import time
import sys
import random
from typing import Literal, overload
from colorama import Fore, Back, Style, init

_LOGO_DUMP = [
"""

""",
]

class Logo:
    def __init__(self, *, autoreset: bool = True, sep: bool | None = False):
        self.autoreset = autoreset
        self.sep = sep

    @overload
    def create(self) -> str | None: ...
    @overload
    def create(self, *, choice: int = 0): ...
    @overload
    def create(self, *, color: str = Fore.RESET): ...
    @overload
    def create(self, *, rand: bool = False): ...
    
    def create(
        self,
        *,
        choice: int = 0,
        color: str = Fore.RESET,
        rand: bool = False
    ):
        if choice and color:
            print(f"{color}{_LOGO_DUMP[choice]}\n")
        elif rand and color:
            if not isinstance(rand, bool): raise TypeError("Invalid type")
