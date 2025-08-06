import sys
from functools import wraps
from io import StringIO
from threading import Thread
from time import sleep


def loading_animation(message=None):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            _chars = ['-', '\\', '|', '/']
            _done = False
            _result = None
            _display_text = (
                message if message is not None else f'Executing {func.__name__}'
            )

            loading_stdout = sys.stdout
            func_stdout = StringIO()
            sys.stdout = func_stdout

            def animate():
                nonlocal _done
                while not _done:
                    for c in _chars:
                        if _done:
                            break
                        loading_stdout.write(f'\r{_display_text}...{c}')
                        loading_stdout.flush()
                        sleep(0.1)
                loading_stdout.write(f'\r{_display_text}...done\n')
                loading_stdout.flush()

            _t = Thread(target=animate)
            _t.start()

            try:
                _result = func(*args, **kwargs)
            finally:
                _done = True
                _t.join()
                sys.stdout = loading_stdout
                print(func_stdout.getvalue(), end='')

            return _result

        return wrapper

    return decorator
