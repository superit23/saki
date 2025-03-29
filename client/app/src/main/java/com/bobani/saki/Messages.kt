package com.bobani.saki

import kotlinx.serialization.*

class SAKIMessageType {
    companion object {
        const val ERROR     = "error"
        const val IMPORT_KEY = "importKey"
        const val IMPORT_KEY_RESULT = "importKeyResult"
        const val GENERATE_KEY = "generateKey"
        const val GENERATE_KEY_RESULT = "generateKeyResult"
        const val GET_ENTRY = "getEntry"
        const val GET_ENTRY_RESULT = "getEntryResult"
        const val LIST_KEYS = "listKeys"
        const val LIST_KEYS_RESULT = "listKeysResult"
        const val ENCRYPT_DATA = "encryptData"
        const val ENCRYPT_DATA_RESULT = "encryptDataResult"
        const val DECRYPT_DATA = "decryptData"
        const val DECRYPT_DATA_RESULT = "decryptDataResult"
        const val SIGN_DATA = "signData"
        const val SIGN_DATA_RESULT = "signDataResult"
        const val VERIFY_SIGNATURE = "verifySignature"
        const val VERIFY_SIGNATURE_RESULT = "verifySignatureResult"
    }
}


@Serializable
data class SAKIMessage(val id: String, val messageType: String, val data: String)

@Serializable
data class SAKIError(val message: String)

@Serializable
data class AlgorithmSpecMessage(val algorithm: String, val keyAlias: String, val purposes: Int, val keySize: Int, val digests: List<String>, val encryptionPaddings: List<String>)

@Serializable
data class GenerateKeyResult(val key: String)

@Serializable
data class GetEntryMessage(val keyAlias: String)

@Serializable
data class GetEntryResult(val key: String, val attributes: List<Pair<String, String>>)

@Serializable
data class ImportKeyMessage(val wrappedKeyAlias: String, val wrappedKey: String, val transformation: String, val spec: AlgorithmSpecMessage)

@Serializable
data class ImportKeyResult(val success: Boolean)

@Serializable
data class ListKeysResult(val keyAliases: List<String>)

@Serializable
data class EncryptDataMessage(val keyAlias: String, val transformation: String, val data: String)

@Serializable
data class EncryptDataResult(val data: String)

@Serializable
data class SignDataMessage(val keyAlias: String, val transformation: String, val data: String)

@Serializable
data class SignDataResult(val signature: String)

@Serializable
data class VerifySignatureMessage(val keyAlias: String, val transformation: String, val data: String, val signature: String)

@Serializable
data class VerifySignatureResult(val verified: Boolean)
