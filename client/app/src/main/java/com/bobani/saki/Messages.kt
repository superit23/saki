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