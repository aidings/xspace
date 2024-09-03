import functools
import sys

class Timeout:
    def __init__(self, sec, prefix=''):
        self.sec = sec
        self.prefix = prefix

    def __call__(self, func):
        @functools.wraps(func)    
        def wrapped_func(*args, **kwargs):
            err_msg = f'Function {func.__name__} timed out after {self.sec} seconds'

            if sys.platform != 'win32':
                import signal

                def _handle_timeout(signum, frame):
                    raise TimeoutError(err_msg)

                signal.signal(signal.SIGALRM, _handle_timeout)
                signal.alarm(self.sec)
                try:
                    result = func(*args, **kwargs)
                finally:
                    signal.alarm(0)
                return result
            else:
                class FuncTimeoutError(TimeoutError):
                    def __init__(self):
                        TimeoutError.__init__(self, err_msg)

                result, exception = [], []

                def run_func():
                    try:
                        res = func(*args, **kwargs)
                    except FuncTimeoutError:
                        pass
                    except Exception as e:
                        exception.append(e)
                    else:
                        result.append(res)

                # typically, a python thread cannot be terminated, use TerminableThread instead
                thread = TerminableThread(target=run_func, daemon=True)
                thread.start()
                thread.join(timeout=sec)

                if thread.is_alive():
                    # a timeout thread keeps alive after join method, terminate and raise TimeoutError
                    exc = type('TimeoutError', FuncTimeoutError.__bases__, dict(FuncTimeoutError.__dict__))
                    thread.terminate(exception_cls=FuncTimeoutError, repeat_sec=raise_sec)
                    raise TimeoutError(err_msg)
                elif exception:
                    # if exception occurs during the thread running, raise it
                    raise exception[0]
                else:
                    # if the thread successfully finished, return its results
                    return result[0]

        return wrapped_func

    def handle_timeout(self, signum, frame):
        raise TimeoutError(f'{self.prefix} timed out after {self.sec} seconds')

    def __enter__(self):
        import signal
        signal.signal(signal.SIGALRM, self.handle_timeout)
        signal.alarm(self.sec)
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        import signal
        signal.alarm(0)
        signal.signal(signal.SIGALRM, signal.SIG_DFL)
