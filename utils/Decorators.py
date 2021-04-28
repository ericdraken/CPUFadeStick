#  Copyright (c) Eric Draken, 2021.
def disabled(f):
    def _decorator(self):
        print(f"{f.__name__} has been disabled")
    return _decorator
