import cProfile
def profile(func):
    def wrapper(*args, **kwargs):
        profiler = cProfile.Profile()
        profiler.enable()
        result = func(*args, **kwargs)
        profiler.disable()
        profiler.print_stats()
        return result
    return wrapper

@profile
def dummy_function(n):
    sum([i**2 for i in range(n)])

dummy_function(100000)
