import sys
import time
from functools import wraps
from .color_print import info
"""
使用python3 -m cProfile your_program.py 更精准的耗时分析
- time.time 提供Epoch到目前的计时,两个时间点的差视为实际流逝的时间长度
- time.perf_counter 可以确保使用系统上面最精确的计时器
- time.process_time 可以确保只计算所在进程花费的CPU时间,即执行时间。
"""


def timer(label='', fmt=':.3f'):
    def func(fun):
        def wrapper(*args, **kwargs):
            start = time.time()
            result = fun(*args, **kwargs)
            cost_time = time.time() - start

            template = "[{}] {}.{} elapsed time: {" + fmt + "}s"
            value = template.format(label, fun.__module__, fun.__name__, cost_time)
            info(value)
            return result
        return wrapper
    return func


class Timer:
    def __init__(self, label='', func=time.perf_counter, output=sys.stdout, fmt=':.3f'):
        self.label = label
        self.output = output
        self._timeit = func
        self._elapsed = 0.0
        self._start = None
        self.fmt = fmt
        self._tcnt = 0 # 计数器

    def start(self, reset=False):
        self._start = self._timeit()
        self._elapsed *= int(reset)
    
    def _update(self, update=True):
        self._tcnt += int(update)

    def stop(self, update_count:bool=False):
        if self._start is None:
            raise RuntimeError("timer not started!")
        end = self._timeit()
        self._elapsed += end - self._start
        self._update(update=update_count)

    def reset(self):
        self._elapsed = 0.0
        self._tcnt = 0

    @property
    def is_running(self):
        return self._start is not None

    @property
    def elapsed(self):
        return self._elapsed

    def running(self, second=False):
        if self._start is None:
            raise RuntimeError('timer not stared!')
        end = self._timeit()
        elapsed = end - self._start

        if not second:
            m, s = divmod(int(elapsed), 60)
            h, m = divmod(m, 60)
            d, h = divmod(h, 24)
            return "{:d}:{:02d}:{:02d}:{:02d}".format(d, h, m, s)
        else:
            return elapsed

    def __call__(self, func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            self.start()
            result = func(*args, **kwargs)
            self.stop(update_count=True)
            template = "[{}] {}.{} elapsed time: {" + self.fmt + "}s"
            value = template.format(self.label, func.__module__, func.__name__, self._elapsed)

            info(value)
            return result
        return wrapper

    def __enter__(self):
        self.start(reset=True)
        return self

    def __exit__(self, *args):
        self.stop(update_count=True)
        template = "[{}] elapsed time: {:.3f}s"
        value = template.format(self.label, self._elapsed)
        info(value)

    def time(self, show=True):
        arevage = self._elapsed / self._tcnt
        if show:
            template = "[{}] elapsed time: {:.3f}s"
            value = template.format(self.label, self._elapsed)
            info(value)
        return arevage

    def speed(self):
        return self._elapsed / self._tcnt
