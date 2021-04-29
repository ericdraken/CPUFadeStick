#  Copyright (c) Eric Draken, 2021.
def disabled(f):
    def _decorator(self):
        print(f"{f.__name__} has been disabled")
    return _decorator


def abstract(f):
    def _decorator(*_):
        raise NotImplementedError(f"Method '{f.__name__}' is abstract")
    return _decorator
