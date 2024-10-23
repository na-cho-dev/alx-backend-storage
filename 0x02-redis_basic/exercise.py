#!/usr/bin/env python3
"""
Writing strings to Redis
"""
from typing import Union
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
