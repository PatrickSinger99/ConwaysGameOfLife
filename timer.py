import time


def debug_timer(func):
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(f"--- {func.__name__}: {round(end - start, 4)}s ---")
        return result

    return wrap
