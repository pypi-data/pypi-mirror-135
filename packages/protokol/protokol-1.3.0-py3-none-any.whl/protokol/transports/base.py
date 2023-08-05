from typing import Callable


class Transport:
    async def connect(self, *urls: str, **kwargs):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def subscribe(self, realm: str, callback: Callable, **kwargs):
        raise NotImplementedError

    async def publish(self, realm, message, **kwargs):
        raise NotImplementedError

    async def request(self, realm, message, **kwargs):
        raise NotImplementedError

    async def monitor(self, callback: Callable, **kwargs):
        raise NotImplementedError

    @property
    def is_connected(self) -> bool:
        """
            Generic property that shows whether the transport connection is "active"
            and able to receive and send data.
            Since this is a property, implementations should avoid altering the state
            and generally stick to read-only flags available at request time.
        :return: whether transport is ready to receive and send data
        """
        raise NotImplementedError
