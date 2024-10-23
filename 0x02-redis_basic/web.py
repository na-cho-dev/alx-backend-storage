#!/usr/bin/env python3
"""
This module contains a function that uses the requests module to obtain
the HTML content of a particular URL and returns it.
"""
import requests
import redis
from functools import wraps
from typing import Callable


cache = redis.Redis()


def cache_page(func: Callable) -> Callable:
    """
    Caches the output of the fetched data
    """
    @wraps(func)
    def wrapper(url: str) -> str:
        """ Wrapper that:
            - check whether a url's data is cached
            - tracks how many times get_page is called
        """
        redis_client = redis.Redis()
        count_key = f'count:{url}'
        content_key = f'content:{url}'

        cached_page = redis_client.get(content_key)
        if cached_page:
            print(f"Cache hit on {url}")
            redis_client.incr(count_key)
            return cached_page.decode('utf-8')

        redis_client.incr(count_key)
        response = func(url)
        redis_client.setex(content_key, 10, response)

        return response

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response
    and tracking the request
    """
    response = requests.get(url)
    return response.text


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    get_page(url)
