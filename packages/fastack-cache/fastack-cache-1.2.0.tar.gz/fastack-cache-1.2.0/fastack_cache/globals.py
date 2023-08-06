from fastack.globals import LocalProxy, state
from starlette.datastructures import State

from fastack_cache.backends.base import BaseCacheBackend


def _get_cache() -> BaseCacheBackend:
    cache = getattr(state, "cache", None)
    if not isinstance(cache, BaseCacheBackend):
        raise RuntimeError("fastack-cache is not installed")
    return cache


def _get_caches() -> BaseCacheBackend:
    caches = getattr(state, "caches", None)
    if not isinstance(caches, State):
        raise RuntimeError("fastack-cache is not installed")
    return caches


cache: BaseCacheBackend = LocalProxy(_get_cache)
caches: State = LocalProxy(_get_caches)
