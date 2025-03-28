from enum import Enum
from base64 import b64decode, b64encode
from dataclasses import dataclass, asdict
from typing import List, Tuple
import uuid
import json
from json import JSONEncoder

class DataClassJSONEncoder(JSONEncoder):
        def default(self, o):
            return asdict(o)


class SAKIException(Exception):
    pass

class SAKIDecodingException(SAKIException):
    pass

class SAKIRemoteException(SAKIException):
    pass

class SAKIMessageType(Enum):
    ERROR               = "error"
    IMPORT_KEY          = "importKey"
    IMPORT_KEY_RESULT   = "importKeyResult"
    GENERATE_KEY        = "generateKey"
    GENERATE_KEY_RESULT = "generateKeyResult"
    GET_ENTRY           = "getEntry"
    GET_ENTRY_RESULT    = "getEntryResult"
    LIST_KEYS           = "listKeys"
    LIST_KEYS_RESULT    = "listKeysResult"


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
        return SAKIMessage(id or str(uuid.uuid4()), self.TYPE.value, json.dumps(self.__dict__, cls=DataClassJSONEncoder))


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


# @dataclass
# class GenerateKeyMessage(SAKISubMessage):
#     TYPE = SAKIMessageType.GENERATE_KEY
#     algorithm: str
#     keyAlias: str
#     purposes: int
#     keySize: int
#     digests: List[str]
#     encryptionPaddings: List[str]


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
