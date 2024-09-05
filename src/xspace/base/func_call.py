from typing import Callable

class FunctionCounter:
    def __init__(self, func:Callable):
        self.func = func
        self.calls = 0
    
    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)
