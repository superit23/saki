from enum import Enum
from dataclasses import dataclass
from typing import List, Tuple
import uuid
import json
from json import JSONEncoder

class DataClassJSONEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__


class SAKIException(Exception):
    pass

class SAKIDecodingException(SAKIException):
    pass

class SAKIRemoteException(SAKIException):
    pass

class SAKIMessageType(Enum):
    ERROR                   = "error"
    IMPORT_KEY              = "importKey"
    IMPORT_KEY_RESULT       = "importKeyResult"
    GENERATE_KEY            = "generateKey"
    GENERATE_KEY_RESULT     = "generateKeyResult"
    GET_ENTRY               = "getEntry"
    GET_ENTRY_RESULT        = "getEntryResult"
    LIST_KEYS               = "listKeys"
    LIST_KEYS_RESULT        = "listKeysResult"
    ENCRYPT_DATA            = "encryptData"
    ENCRYPT_DATA_RESULT     = "encryptDataResult"
    DECRYPT_DATA            = "decryptData"
    DECRYPT_DATA_RESULT     = "decryptDataResult"
    SIGN_DATA               = "signData"
    SIGN_DATA_RESULT        = "signDataResult"
    VERIFY_SIGNATURE        = "verifySignature"
    VERIFY_SIGNATURE_RESULT = "verifySignatureResult"
    

@dataclass
class SAKIMessage(object):
    id: str
    messageType: str
    data: dict

    def encode(self):
        return json.dumps(self.__dict__, cls=DataClassJSONEncoder)
    

    @staticmethod
    def decode(message: str):
        return SAKISubMessage.decode(message)


class SAKISubMessage(object):
    TYPE = None

    def build_message(self, id: str=None):
        return SAKIMessage(id or str(uuid.uuid4()), self.TYPE.value, json.dumps(self, cls=DataClassJSONEncoder))


    @staticmethod
    def decode(message: str):
        saki_msg = json.loads(message)

        for subclass in SAKISubMessage.__subclasses__():
            if subclass.TYPE.value == saki_msg['messageType']:
                return subclass(**json.loads(saki_msg['data']))
        
        raise SAKIDecodingException(f"Unknown request type: {saki_msg['messageType']}")



@dataclass
class SAKIError(SAKISubMessage):
    TYPE = SAKIMessageType.ERROR
    message: str


@dataclass
class AlgorithmSpecMessage(SAKISubMessage):
    TYPE = SAKIMessageType.GENERATE_KEY
    algorithm: str
    keyAlias: str
    purposes: int
    keySize: int
    digests: List[str]
    encryptionPaddings: List[str]


@dataclass
class ImportKeyMessage(SAKISubMessage):
    TYPE = SAKIMessageType.IMPORT_KEY
    wrappedKeyAlias: str
    wrappedKey: str
    transformation: str
    spec: AlgorithmSpecMessage


@dataclass
class ImportKeyResult(SAKISubMessage):
    TYPE = SAKIMessageType.IMPORT_KEY_RESULT
    success: bool


@dataclass
class GenerateKeyResult(SAKISubMessage):
    TYPE = SAKIMessageType.GENERATE_KEY_RESULT
    key: str


@dataclass
class GetEntryMessage(SAKISubMessage):
    TYPE = SAKIMessageType.GET_ENTRY
    keyAlias: str


@dataclass
class GetEntryResult(SAKISubMessage):
    TYPE = SAKIMessageType.GET_ENTRY_RESULT
    key: str
    attributes: List[Tuple[str, str]]


@dataclass
class ListKeysMessage(SAKISubMessage):
    TYPE = SAKIMessageType.LIST_KEYS


@dataclass
class ListKeysResult(SAKISubMessage):
    TYPE = SAKIMessageType.LIST_KEYS_RESULT
    keyAliases: List[str]


@dataclass
class EncryptDataMessage(SAKISubMessage):
    TYPE = SAKIMessageType.ENCRYPT_DATA
    keyAlias: str
    transformation: str
    data: str


@dataclass
class EncryptDataResult(SAKISubMessage):
    TYPE = SAKIMessageType.ENCRYPT_DATA_RESULT
    data: str


@dataclass
class DecryptDataMessage(SAKISubMessage):
    TYPE = SAKIMessageType.DECRYPT_DATA
    keyAlias: str
    transformation: str
    data: str


@dataclass
class DecryptDataResult(SAKISubMessage):
    TYPE = SAKIMessageType.DECRYPT_DATA_RESULT
    data: str


@dataclass
class SignDataMessage(SAKISubMessage):
    TYPE = SAKIMessageType.SIGN_DATA
    keyAlias: str
    transformation: str
    data: str


@dataclass
class SignDataResultMessage(SAKISubMessage):
    TYPE = SAKIMessageType.SIGN_DATA_RESULT
    signature: str


@dataclass
class VerifySignatureMessage(SAKISubMessage):
    TYPE = SAKIMessageType.VERIFY_SIGNATURE
    keyAlias: str
    transformation: str
    data: str
    signature: str


@dataclass
class VerifySignatureResult(SAKISubMessage):
    TYPE = SAKIMessageType.VERIFY_SIGNATURE_RESULT
    verified: bool
