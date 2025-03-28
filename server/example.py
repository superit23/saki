# NOTE: This is designed to be ran within samson
from saki.messages import *
from saki.key_properties import KeyProperties
from saki.proxy_object import KeyStore
from saki.server import SAKIServer

# Start SAKI server
server = SAKIServer()
server.start()


################################################################################
# STEP 1: Generate temporary wrapping key, import our own wrapping key with it #
################################################################################

# Constants
IMPORT_KEY_ALIAS   = "importtest2"
WRAPPING_KEY_ALIAS = "testkey2"
WRAP_TRANSFORM     = "RSA/ECB/OAEPPadding"
KEY_SIZE           = 2048
WRAPPING_KEY_SPEC  = AlgorithmSpecMessage(
    algorithm=KeyProperties.KEY_ALGORITHM_RSA.value,
    keyAlias=WRAPPING_KEY_ALIAS,
    purposes=KeyProperties.PURPOSE_WRAP_KEY.value,
    keySize=KEY_SIZE,
    digests=[KeyProperties.DIGEST_SHA256.value],
    encryptionPaddings=[KeyProperties.ENCRYPTION_PADDING_RSA_OAEP.value]
)

# Generate new wrapping key in keystore
keystore     = KeyStore(server.connection)
public_key   = keystore.generate_key(**WRAPPING_KEY_SPEC.__dict__)
wrapping_key = PKIAutoParser.import_key(public_key.key.encode('utf-8')).key

# Create new key and wrap it
rsa     = RSA(KEY_SIZE)
wrapped = rsa.export_private_key(PKIEncoding.ANDROID_KW, wrapping_key=wrapping_key).encode()
encoded = EncodingScheme.BASE64.encode(wrapped)

# Import key into keystore instead of the wrapping key
result1 = keystore.import_key(WRAPPING_KEY_ALIAS, encoded.decode(), WRAP_TRANSFORM, WRAPPING_KEY_SPEC)


###############################################################
# STEP 2: Wrap a new key using our wrapping key and import it #
###############################################################

# Pull wrapping key from keystore
public_key   = keystore.get_entry(WRAPPING_KEY_ALIAS)
wrapping_key = PKIAutoParser.import_key(public_key.key.encode('utf-8')).key

# Create new key and wrap it using OUR WRAPPING KEY
ec      = ECDSA(P256.G)
wrapped = ec.export_private_key(PKIEncoding.ANDROID_KW, wrapping_key=wrapping_key).encode()
encoded = EncodingScheme.BASE64.encode(wrapped)

# Import key into keystore
result2 = keystore.import_key(IMPORT_KEY_ALIAS, encoded.decode(), WRAP_TRANSFORM, WRAPPING_KEY_SPEC)
print(wrapping_key.n == rsa.n and result1.success and result2.success)