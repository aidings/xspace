from typing import Callable

class FunctionCounter:
    """ Count the number of calls of a function. used as a decorator.

        Args:
            func (Callable): a function or a method module
    """
    def __init__(self, func:Callable):
        self.func = func
        self.calls = 0
    
    def __call__(self, *args, **kwargs):
        self.calls += 1
        return self.func(*args, **kwargs)
