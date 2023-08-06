from typing import Coroutine

import anyio
from fastack.globals import request as _g_request
from fastapi import Request

from fastack_cache.backends.base import BaseCacheBackend


def get_request_object(kwargs: dict) -> Request:
    request: Request = None
    for _, v in kwargs.items():
        if isinstance(v, Request):
            request = v
            break

    if not request:
        request = _g_request

    return request


def get_cache_backend(request: Request, cache: str = "default") -> BaseCacheBackend:
    cache_backend: BaseCacheBackend = request.state.caches._state[cache]
    return cache_backend


def run_sync(func: Coroutine, *args, **kwds):
    async def executor():
        return await func(*args, **kwds)

    return anyio.from_thread.run(executor)
