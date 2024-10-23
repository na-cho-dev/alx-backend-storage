#!/usr/bin/env python3
"""
Writing strings to Redis
"""
from typing import Union, Callable, Optional
from functools import wraps
import redis
import uuid


def count_calls(fn: Callable) -> Callable:
    """
    A decorator that counts how many times a
    function in Cache class is called.
    
    :param fn: The function to be decorated.
    :return: The decorated function.
    """
    @wraps(fn)
    def wrapper(self, *args, **kwargs):
        key = fn.__qualname__
        self._redis.incr(key)
        return fn(self, *args, **kwargs)

    return wrapper
        

class Cache:
    """
    The Cache class writes strings to Redis
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

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
