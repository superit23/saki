# NOTE: These examples are designed to be ran within samson
from saki.messages import *
from saki.key_properties import KeyProperties
from saki.proxy_object import KeyStore
from saki.server import SAKIServer

# Start SAKI server
server = SAKIServer()
server.start()


##############################################################################
# Ex 1: Generate temporary wrapping key, import our own wrapping key with it #
##############################################################################
WRAPPING_KEY_ALIAS  = "testkey2"
WRAP_TRANSFORM      = "RSA/ECB/OAEPPadding"
KEY_SIZE            = 2048
WRAPPING_KEY_SPEC   = AlgorithmSpecMessage(
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
wrapping_key = PKIAutoParser.import_key(public_key).key

# Create new key and wrap it
rsa     = RSA(KEY_SIZE)
wrapped = rsa.export_private_key(PKIEncoding.ANDROID_KW, wrapping_key=wrapping_key).encode()

# Import key into keystore instead of the wrapping key
success = keystore.import_key(WRAPPING_KEY_ALIAS, wrapped, WRAP_TRANSFORM, WRAPPING_KEY_SPEC)
assert success



####################################################################
# Ex 2: Wrap a new EC key using our RSA wrapping key and import it #
####################################################################
WRAPPING_KEY_ALIAS = "testkey2"
EC_SIGNING_ALIAS   = "ectest1"
KEY_SIZE           = 2048
WRAPPING_KEY_SPEC  = AlgorithmSpecMessage(
    algorithm=KeyProperties.KEY_ALGORITHM_RSA.value,
    keyAlias=WRAPPING_KEY_ALIAS,
    purposes=KeyProperties.PURPOSE_WRAP_KEY.value,
    keySize=KEY_SIZE,
    digests=[KeyProperties.DIGEST_SHA256.value],
    encryptionPaddings=[KeyProperties.ENCRYPTION_PADDING_RSA_OAEP.value]
)

# Pull wrapping key from keystore
keystore     = KeyStore(server.connection)
public_key   = keystore.get_entry(WRAPPING_KEY_ALIAS)
wrapping_key = PKIAutoParser.import_key(public_key).key

# Create new key and wrap it using OUR WRAPPING KEY
ec      = ECDSA(P256.G)
wrapped = ec.export_private_key(PKIEncoding.ANDROID_KW, wrapping_key=wrapping_key).encode()

# Import key into keystore
result = keystore.import_key(EC_SIGNING_ALIAS, wrapped, WRAP_TRANSFORM, WRAPPING_KEY_SPEC)
assert success and wrapping_key.n == rsa.n



##########################################
# Ex 3: Sign/verify data with the EC key #
##########################################
DATA_TO_SIGN        = b'This is my data!'
SIGNATURE_TRANSFORM = "SHA256withECDSA"
EC_SIGNING_ALIAS    = "ectest1"

# Sign and verify
keystore  = KeyStore(server.connection)
signature = keystore.sign_data(EC_SIGNING_ALIAS, SIGNATURE_TRANSFORM, DATA_TO_SIGN)
verified  = keystore.verify_signature(EC_SIGNING_ALIAS, SIGNATURE_TRANSFORM, DATA_TO_SIGN, signature)
assert verified



#########################################
# STEP 4: Encrypt/decrypt data with RSA #
#########################################
ENCRYPTION_KEY       = "testkey2"
ENCRYPTION_TRANSFORM = "RSA/ECB/OAEPPadding"
DATA_TO_ENCRYPT      = b'This is my data!'

# Encrypt and decrypt
keystore   = KeyStore(server.connection)
ciphertext = keystore.encrypt_data(ENCRYPTION_KEY, ENCRYPTION_TRANSFORM, DATA_TO_ENCRYPT)
plaintext  = keystore.decrypt_data(ENCRYPTION_KEY, ENCRYPTION_TRANSFORM, ciphertext)
assert plaintext == DATA_TO_ENCRYPT
