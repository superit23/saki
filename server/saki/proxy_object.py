from saki.messages import *
from queue import Queue, Empty
from base64 import b64decode, b64encode
import uuid


def base64_encode(val: str):
    return b64encode(val).decode()

def base64_decode(val: str):
    return b64decode(val.encode('utf-8'))


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

    def import_key(self, wrappedKeyAlias: str, wrappedKey: bytes, transformation: str, spec: AlgorithmSpecMessage):
        return self._proxy_function(ImportKeyMessage, wrappedKeyAlias, base64_encode(wrappedKey), transformation, spec).success

    def generate_key(self, *args, **kwargs):
        key = self._proxy_function(AlgorithmSpecMessage, *args, **kwargs).key
        return base64_decode(key)

    def aliases(self, *args, **kwargs):
        return self._proxy_function(ListKeysMessage, *args, **kwargs).keyAliases

    def get_entry(self, *args, **kwargs):
        key = self._proxy_function(GetEntryMessage, *args, **kwargs).key
        return base64_decode(key)

    def encrypt_data(self, keyAlias: str, transformation: str, data: bytes):
        ciphertext = self._proxy_function(EncryptDataMessage, keyAlias, transformation, base64_encode(data)).data
        return base64_decode(ciphertext)

    def decrypt_data(self, keyAlias: str, transformation: str, data: bytes):
        plaintext = self._proxy_function(DecryptDataMessage, keyAlias, transformation, base64_encode(data)).data
        return base64_decode(ciphertext)

    def sign_data(self, keyAlias: str, transformation: str, data: bytes):
        signature = self._proxy_function(SignDataMessage, keyAlias, transformation, base64_encode(data)).signature
        return base64_decode(signature)

    def verify_signature(self, keyAlias: str, transformation: str, data: bytes, signature: bytes):
        return self._proxy_function(VerifySignatureMessage, keyAlias, transformation, base64_encode(data), base64_encode(signature)).verified
