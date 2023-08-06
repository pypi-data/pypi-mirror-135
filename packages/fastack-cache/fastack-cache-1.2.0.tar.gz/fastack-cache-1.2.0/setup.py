# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fastack_cache', 'fastack_cache.backends', 'fastack_cache.serializers']

package_data = \
{'': ['*']}

install_requires = \
['fastack>=4.0.0,<5.0.0']

extras_require = \
{'aioredis': ['aioredis>=2.0.1,<3.0.0'], 'redis': ['redis>=4.1.1,<5.0.0']}

setup_kwargs = {
    'name': 'fastack-cache',
    'version': '1.2.0',
    'description': 'Caching plugin for fastack',
    'long_description': '# fastack-cache\n\nfastack-cache is a caching plugin for [fastack](https://github.com/fastack-dev/fastack) ❤️\n\nThis plugin is inspired by the [django cache framework](https://docs.djangoproject.com/en/4.0/topics/cache/) and [django-redis](https://github.com/jazzband/django-redis)!\n\nSupported cache backend:\n\n* Redis:\n    * ``fastack_cache.backends.redis.RedisBackend`` - Sync version\n    * ``fastack_cache.backends.aioredis.AioRedisBackend`` - Async version\n\n# Installation\n\n```\npip install -U fastack-cache\n```\n\n# Usage\n\nAdd the plugin to your project configuration:\n\n```python\nPLUGINS = [\n    "fastack_cache",\n    ...\n]\n```\n\nConfiguration:\n\n```python\nREDIS_HOST = "localhost"\nREDIS_PORT = 6900\nREDIS_DB = 0\nCACHES = {\n    # cache name\n    "default": {\n        # cache backend\n        "BACKEND": "fastack_cache.backends.redis.RedisBackend",\n        # Cache options to be passed to the Redis(...) class\n        "OPTIONS": {\n            "host": REDIS_HOST,\n            "port": REDIS_PORT,\n            "db": REDIS_DB,\n        },\n        # Serializer for converting data into cache\n        "SERIALIZER": {\n            "CLASS": "fastack_cache.serializers.JSONSerializer",\n            "OPTIONS": {\n                # Option to pass when dumps() method in serializer class is called\n                "DUMPS": {},\n                # Option to pass when loads() method in serializer class is called\n                "LOADS": {}\n            }\n        }\n    }\n}\n```\n',
    'author': 'aprilahijriyan',
    'author_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'maintainer': 'aprilahijriyan',
    'maintainer_email': '37798612+aprilahijriyan@users.noreply.github.com',
    'url': 'https://github.com/fastack-dev/fastack-cache',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'extras_require': extras_require,
    'python_requires': '>=3.7,<3.10',
}


setup(**setup_kwargs)
