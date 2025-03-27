# from saki.messages import *
from queue import Queue, Empty
import uuid

class ProxyObject(object):
    def __init__(self, connection, id: str=None):
        self.id = id or str(uuid.uuid4())
        self.connection = connection
        self.queue = Queue()


    def _proxy_function(self, message_type, *args, **kwargs):
        return self._perform_request(message_type(*args, **kwargs))


    def _perform_request(self, msg):
        self.connection.request_queue.put((self, msg))
        result = self.queue.get()

        if result.TYPE == SAKIMessageType.ERROR:
            raise SAKIRemoteException(result.message)

        return result


class KeyStore(ProxyObject):

    def import_key(self, *args, **kwargs):
        return self._proxy_function(ImportKeyMessage, *args, **kwargs)

    def generate_key(self, *args, **kwargs):
        return self._proxy_function(GenerateKeyMessage, *args, **kwargs)

    def aliases(self, *args, **kwargs):
        return self._proxy_function(ListKeysMessage, *args, **kwargs)

    def get_entry(self, *args, **kwargs):
        return self._proxy_function(GetEntryMessage, *args, **kwargs)
