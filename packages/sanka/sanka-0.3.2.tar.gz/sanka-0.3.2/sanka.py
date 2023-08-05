from functools import partial
from typing import Callable
from typing import TypeVar


T = TypeVar('T')

class Sanka:

    def __init__(
        self,
        func: Callable,
        callback: Callable[[int], T] = None,
        cumulative: bool = True,
        only_callback_when_dead: bool = True
    ):
        if callback and not callable(callback):
            raise TypeError(f'Callback must be Callable not "{type(callback).__name__}"')

        self.func = func
        self.calls = 0
        self.callback = callback
        self.cumulative = cumulative
        self.only_callback_when_dead = only_callback_when_dead

    def __get__(self, instance, owner):
        return partial(self, instance)

    def __call__(self, *args, **kwargs):
        if YaDead in args:
            if self.callback and self.only_callback_when_dead:
                self.callback(self.calls)
            return self.calls
        else:
            result = self.func(*args, **kwargs)
            if self.cumulative:
                self.calls += 1
            else:
                self.calls = 1

            if self.callback and not self.only_callback_when_dead:
                self.callback(self.calls)

            return result

    def __repr__(self):
        return f'<Sanka({self.func.__name__}), calls: {self.calls}>'

    def __str__(self):
        return self.func.__name__


def sanka(
    function: Callable = None,
    callback: Callable[[int], T] = None,
    cumulative: bool = True,
    only_callback_when_dead: bool = True
):
    if function:
        return Sanka(function)
    else:
        def wrapper(function):
            return Sanka(function, callback, cumulative, only_callback_when_dead)
        return wrapper


class YaDead:
    pass

