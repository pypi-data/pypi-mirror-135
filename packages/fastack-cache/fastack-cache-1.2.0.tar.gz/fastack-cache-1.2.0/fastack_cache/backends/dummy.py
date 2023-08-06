from fastack_cache.backends.base import BaseCacheBackend


class DummyBackend(BaseCacheBackend):
    def __init__(self, serializer, **options):
        super().__init__(serializer, **options)

    def connect(self) -> "DummyBackend":
        """
        Connect to the server.
        """

    def disconnect(self) -> None:
        """
        Disconnect from the server.
        """

    def get(self, key):
        pass

    def set(self, key, value, timeout=None):
        pass

    def delete(self, key):
        pass

    def clear(self):
        pass
