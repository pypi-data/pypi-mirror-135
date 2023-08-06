# fastack-cache

fastack-cache is a caching plugin for [fastack](https://github.com/fastack-dev/fastack) ❤️

This plugin is inspired by the [django cache framework](https://docs.djangoproject.com/en/4.0/topics/cache/) and [django-redis](https://github.com/jazzband/django-redis)!

Supported cache backend:

* Redis:
    * ``fastack_cache.backends.redis.RedisBackend`` - Sync version
    * ``fastack_cache.backends.aioredis.AioRedisBackend`` - Async version

# Installation

```
pip install -U fastack-cache
```

# Usage

Add the plugin to your project configuration:

```python
PLUGINS = [
    "fastack_cache",
    ...
]
```

Configuration:

```python
REDIS_HOST = "localhost"
REDIS_PORT = 6900
REDIS_DB = 0
CACHES = {
    # cache name
    "default": {
        # cache backend
        "BACKEND": "fastack_cache.backends.redis.RedisBackend",
        # Cache options to be passed to the Redis(...) class
        "OPTIONS": {
            "host": REDIS_HOST,
            "port": REDIS_PORT,
            "db": REDIS_DB,
        },
        # Serializer for converting data into cache
        "SERIALIZER": {
            "CLASS": "fastack_cache.serializers.JSONSerializer",
            "OPTIONS": {
                # Option to pass when dumps() method in serializer class is called
                "DUMPS": {},
                # Option to pass when loads() method in serializer class is called
                "LOADS": {}
            }
        }
    }
}
```
