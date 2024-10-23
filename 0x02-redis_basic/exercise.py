#!/usr/bin/env python3
"""
Writing strings to Redis
"""
from typing import Union, Callable, Optional
from functools import wraps
import redis
import uuid


def count_calls(method: Callable) -> Callable:
    """
    A decorator that counts how many times a
    function in Cache class is called.

    :param fn: The function to be decorated.
    :return: The decorated function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Decorator to count the number of times a method is called
        """
        key = method.__qualname__

        if isinstance(self._redis, redis.Redis):
            self._redis.incr(key)
        return method(self, *args, **kwargs)

    return wrapper


def call_history(method: Callable) -> Callable:
    """
    A decorator that store the history of inputs and outputs
    for a particular function

    :param fn: The function to be decorated.
    :return: The decorated function.
    """
    @wraps(method)
    def wrapper(self, *args, **kwargs):
        """
        Decorator to store the history of inputs and outputs
        for a particular function
        """
        input_key = f"{method.__qualname__}:inputs"
        output_key = f"{method.__qualname__}:outputs"

        self._redis.rpush(input_key, str(args))
        method_output = method(self, *args, **kwargs)
        self._redis.rpush(output_key, str(method_output))

        return method_output
    return wrapper


def replay(method: Callable) -> None:
    """
    Display the history of calls for a given method.
    """
    redis_client = method.__self__._redis
    method_name = method.__qualname__
    call_count = redis_client.get(method_name)

    if call_count is None:
        print(f"{method_name} was never called")
        return

    call_count = int(call_count.decode("utf-8"))
    print(f"{method_name} was called {call_count} times:")

    input_key = method_name + ":inputs"
    output_key = method_name + ":outputs"
    inputs = redis_client.lrange(input_key, 0, -1)
    outputs = redis_client.lrange(output_key, 0, -1)

    for inp, outp in zip(inputs, outputs):
        input_str = inp.decode('utf-8')
        output_str = outp.decode('utf-8')
        print(f"{method_name}(*{input_str}) -> {output_str}")


class Cache:
    """
    The Cache class writes strings to Redis
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    @call_history
    @count_calls
    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using the random key
        and return the key.
        """
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)

        return rand_key

    def get(self, key: str, fn: Optional[Callable[[bytes], any]] = None):
        """
        Gets value from Redis with key passed in as argument
        """
        value = self._redis.get(key)

        if fn:
            return fn(value)

        return value

    def get_str(self, val):
        """
        Converts and returns val as string
        """
        return str(val)

    def get_int(self, val):
        """
        Converts and returns val as int
        """
        return int(val)
