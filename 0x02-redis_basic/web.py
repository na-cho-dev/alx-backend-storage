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
        try:
            cached_page = cache.get(f"content:{url}")
            if cached_page:
                print(f"Cache hit for URL: {url}")
                return cached_page.decode('utf-8')

            content = func(url)
            cache.setex(f"content:{url}", 10, content)
            cache.incr(f"count:{url}")
            return content

        except requests.RequestException as e:
            print(f"Error fetching the page: {e}")
            return "An error occurred while fetching page."

    return wrapper


@cache_page
def get_page(url: str) -> str:
    """
    Returns the content of a URL after caching the request's response
    and tracking the request
    """
    try:
        response = requests.get(url)
        response.raise_for_status()
        return response.text
    except requests.RequestException as e:
        return f"Error fetching the page: {e}"


if __name__ == "__main__":
    url = "http://slowwly.robertomurray.co.uk"
    get_page(url)
