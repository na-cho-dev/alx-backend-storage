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


def cache_page(fn: Callable) -> Callable:
    """
    Caches the output of the fetched data
    """
    @wraps(fn)
    def wrapper(url: str) -> str:
        """ Wrapper that:
            - check whether a url's data is cached
            - tracks how many times get_page is called
        """
        client = redis.Redis()
        client.incr(f'count:{url}')
        cached_page = client.get(f'{url}')
        if cached_page:
            return cached_page.decode('utf-8')
        response = fn(url)
        client.set(f'{url}', response, 10)
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
