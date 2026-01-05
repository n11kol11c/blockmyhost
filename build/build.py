import json
import os, sys
import time
import string 
import math
import typing
from typing import Callable, Literal, overload, Any

class Build:
    Mods = Literal['a', 'w', 'rb']
    JSON_BUILD_FILE = "build.json"
    
    def __init__(self, file: str, content: str = ""):
        self.file = file
        self.content = content
        
    def read(self, m: Mods, error: bool | None = None) -> str:
        try:
            with open(self.file, mode=m, errors=error) as f:
                self.content = "".join(json.loads(f))
            
            if len(self.content) <= 0: 
                raise Exception("Json build file is empty or not found.")
            else: return self.content
            
        except FileNotFoundError as err:
            raise Exception(err)
        
        finally: pass
        
