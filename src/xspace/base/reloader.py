from loguru import logger

class Reloader:
    def __init__(self, load_func, style=None):
        self.style = style
        self.load_func = load_func
    
    def __call__(self, *args, style, **kwargs):
        if style != self.style:
            logger.debug(f"Reloading {self.load_func.__name__} with style {style}")
            self.load_func(*args, **kwargs) 
            self.style = style
            logger.debug(f"Reloaded {self.load_func.__name__} with style {style} successfully")