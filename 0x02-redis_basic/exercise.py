#!/usr/bin/env python3
"""this is a module"""

import redis
from uuid import uuid4
from typing import Union, Callable, Optional
from functools import wraps


def count_calls(method: Callable) -> Callable:
    """this is a function"""
    key = method.__qualname__

    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """this is a function"""
        self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """this is a function"""
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """this is a function"""
        input = str(args)
        self._redis.rpush(method.__qualname__ + ":inputs", input)
        output = str(method(self, *args, **kwargs))
        self._redis.rpush(method.__qualname__ + ":outputs", output)
        return output

    return wrapper


def replay(fn: Callable):
    """this is a function"""
    r = redis.Redis()
    function_name = fn.__qualname__
    value = r.get(function_name)
    try:
        value = int(value.decode("utf-8"))
    except Exception:
        value = 0

    # print(f"{function_name} was called {value} times")
    print("{} was called {} times:".format(function_name, value))
    # inputs = r.lrange(f"{function_name}:inputs", 0, -1)
    inputs = r.lrange("{}:inputs".format(function_name), 0, -1)

    # outputs = r.lrange(f"{function_name}:outputs", 0, -1)
    outputs = r.lrange("{}:outputs".format(function_name), 0, -1)

    for input, output in zip(inputs, outputs):
        try:
            input = input.decode("utf-8")
        except Exception:
            input = ""

        try:
            output = output.decode("utf-8")
        except Exception:
            output = ""

        # print(f"{function_name}(*{input}) -> {output}")
        print("{}(*{}) -> {}".format(function_name, input, output))


class Cache:
    """a class"""

    def __init__(self):
        """this is a function"""
        self._redis = redis.Redis()
        self._redis.flushdb()

    @count_calls
    @call_history
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """this is a function"""
        random_key = str(uuid4())
        self._redis.set(random_key, data)
        return random_key

    def get(self, key: str,
            fn: Optional[callable] = None) -> Union[str, bytes, int, float]:
        """this is a function"""
        value = self._redis.get(key)
        if fn:
            value = fn(value)
        return value

    def get_str(self, key: str) -> str:
        """this is a function"""
        value = self._redis.get(key)
        return value.decode("utf-8")

    def get_int(self, key: str) -> int:
        """this is a function"""
        value = self._redis.get(key)
        try:
            value = int(value.decode("utf-8"))
        except Exception:
            value = 0
        return value
