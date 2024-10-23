#!/usr/bin/env python3
"""
Writing strings to Redis
"""
from typing import Union, Callable, Optional
import redis
import uuid


class Cache:
    """
    The Cache class writes strings to Redis
    """
    def __init__(self):
        self._redis = redis.Redis()
        self._redis.flushdb()

    def store(self, data: Union[str, bytes, int, float]) -> str:
        """
        Store the input data in Redis using the random key
        and return the key.
        """
        rand_key = str(uuid.uuid4())
        self._redis.set(rand_key, data)

        return rand_key
    
    def get(self, key: str, fn: Optional[Callable[[bytes], any]] = None):
        value = self._redis.get(key)
        
        if value is None:
            return None

        if fn:
            return fn(value)
        
        return value

    def get_str(self, val):
        return str(val)

    def get_int(self, val):
        return int(val)
