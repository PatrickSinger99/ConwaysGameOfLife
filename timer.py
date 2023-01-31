import time


def debug_timer(func):
    def wrap(*args, **kwargs):
        start = time.time()
        result = func(*args, **kwargs)
        end = time.time()

        print(f"[DEBUG] {func.__name__}: {round(end - start, 3)}s")
        return result

    return wrap
