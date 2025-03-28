from enum import Enum

# https://android.googlesource.com/platform/frameworks/base/+/master/keystore/java/android/security/keystore/KeyProperties.java
# Ripped straight outta Java ;)
# NOTE! While these values _correspond_ to the KeymasterDefs in the AndroidKeyStore, these are different constants. They are converted
# into an AuthorizationList inside of Android
class KeyProperties(Enum):
    AUTH_DEVICE_CREDENTIAL = 1 << 0
    AUTH_BIOMETRIC_STRONG = 1 << 1
    PURPOSE_ENCRYPT = 1 << 0
    PURPOSE_DECRYPT = 1 << 1
    PURPOSE_SIGN = 1 << 2
    PURPOSE_VERIFY = 1 << 3
    PURPOSE_WRAP_KEY = 1 << 5
    PURPOSE_AGREE_KEY = 1 << 6
    PURPOSE_ATTEST_KEY = 1 << 7
    KEY_ALGORITHM_RSA = "RSA"
    KEY_ALGORITHM_EC = "EC"
    KEY_ALGORITHM_XDH = "XDH"
    KEY_ALGORITHM_AES = "AES"
    KEY_ALGORITHM_3DES = "DESede"
    KEY_ALGORITHM_HMAC_SHA1 = "HmacSHA1"
    KEY_ALGORITHM_HMAC_SHA224 = "HmacSHA224"
    KEY_ALGORITHM_HMAC_SHA256 = "HmacSHA256"
    KEY_ALGORITHM_HMAC_SHA384 = "HmacSHA384"
    KEY_ALGORITHM_HMAC_SHA512 = "HmacSHA512"
    BLOCK_MODE_ECB = "ECB"
    BLOCK_MODE_CBC = "CBC"
    BLOCK_MODE_CTR = "CTR"
    BLOCK_MODE_GCM = "GCM"
    ENCRYPTION_PADDING_NONE = "NoPadding"
    ENCRYPTION_PADDING_PKCS7 = "PKCS7Padding"
    ENCRYPTION_PADDING_RSA_PKCS1 = "PKCS1Padding"
    ENCRYPTION_PADDING_RSA_OAEP = "OAEPPadding"
    SIGNATURE_PADDING_RSA_PKCS1 = "PKCS1"
    SIGNATURE_PADDING_RSA_PSS = "PSS"
    DIGEST_NONE = "NONE"
    DIGEST_MD5 = "MD5"
    DIGEST_SHA1 = "SHA-1"
    DIGEST_SHA224 = "SHA-224"
    DIGEST_SHA256 = "SHA-256"
    DIGEST_SHA384 = "SHA-384"
    DIGEST_SHA512 = "SHA-512"
    ORIGIN_GENERATED = 1 << 0
    ORIGIN_IMPORTED = 1 << 1
    ORIGIN_UNKNOWN = 1 << 2
    ORIGIN_SECURELY_IMPORTED = 1 << 3
    SECURITY_LEVEL_UNKNOWN = -2
    SECURITY_LEVEL_UNKNOWN_SECURE = -1
    SECURITY_LEVEL_SOFTWARE = 0
    SECURITY_LEVEL_TRUSTED_ENVIRONMENT = 1
    SECURITY_LEVEL_STRONGBOX = 2
    NAMESPACE_APPLICATION = -1
    NAMESPACE_WIFI = 102
    NAMESPACE_LOCKSETTINGS = 103
    UID_SELF = -1
    UNRESTRICTED_USAGE_COUNT = -1