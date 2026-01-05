import time
from typing import Callable
from functools import wraps

class Uptime:
    _start_time: float | None = None

    @classmethod
    def set(cls):
        def decorator(func: Callable):
            @wraps(func)
            def wrapper(*args, **kwargs):
                cls._start_time = time.time()
                try:
                    return func(*args, **kwargs)
                finally:
                    uptime = time.time() - cls._start_time
                    print(f"Program uptime: {uptime:.3f} seconds")
            return wrapper
        return decorator
