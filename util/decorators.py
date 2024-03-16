import functools
import time


def non_null_args(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        for arg in args:
            if not arg:
                raise ValueError(
                    "Arguments to function: {} cannot be None".format(func.__name__)
                )

        for kwarg in kwargs.values():
            if not kwarg:
                raise ValueError(
                    "Arguments to function: {} cannot be None".format(func.__name__)
                )

        return func(*args, **kwargs)

    return wrapper


def add_pre_delay(_func=None, *, delay=1):
    def decorator_delay(func):
        @functools.wraps(func)
        def wrapper(*args, **kwargs):
            time.sleep(delay)
            return func(*args, **kwargs)

        return wrapper

    if not _func:
        return decorator_delay
    else:
        return decorator_delay(_func)


def run_indefinitely(func):
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        while True:
            func(*args, **kwargs)

    return wrapper
