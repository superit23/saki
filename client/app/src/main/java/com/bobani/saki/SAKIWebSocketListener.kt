package com.bobani.saki

import android.annotation.SuppressLint
import android.security.keystore.KeyGenParameterSpec
import android.security.keystore.WrappedKeyEntry
import android.util.Log
import okhttp3.Response
import okhttp3.WebSocket
import okhttp3.WebSocketListener
import kotlinx.serialization.json.Json
import java.util.Base64

import java.security.KeyStore
import android.security.keystore.KeyProperties
import kotlinx.coroutines.Job
import java.security.KeyPairGenerator
import java.security.spec.AlgorithmParameterSpec

class SAKIWebSocketListener: WebSocketListener() {

    private val TAG = "Test"

    override fun onOpen(webSocket: WebSocket, response: Response) {
        super.onOpen(webSocket, response)
        Log.d(TAG, "onOpen:")
    }

    override fun onMessage(webSocket: WebSocket, text: String) {
        super.onMessage(webSocket, text)
        Log.d(TAG, "Request: $text")

        val message = Json.decodeFromString<SAKIMessage>(text)
        val result = try {
            handleMessage(message)
        } catch (e: Exception) {
            SAKIMessage(message.id, SAKIMessageType.ERROR, Json.encodeToString(SAKIError(e.message.orEmpty())))
        }

        val response = Json.encodeToString(result)
        webSocket.send(response)

        Log.d(TAG, "Response: $response")
    }

    override fun onClosing(webSocket: WebSocket, code: Int, reason: String) {
        super.onClosing(webSocket, code, reason)
        Log.d(TAG, "onClosing: $code $reason")
    }

    override fun onClosed(webSocket: WebSocket, code: Int, reason: String) {
        super.onClosed(webSocket, code, reason)
        Log.d(TAG, "onClosed: $code $reason")
    }

    override fun onFailure(webSocket: WebSocket, t: Throwable, response: Response?) {
        Log.d(TAG, "onFailure: ${t.message} $response")
        super.onFailure(webSocket, t, response)
    }

    fun handleMessage(message: SAKIMessage): SAKIMessage {
        return when(message.messageType) {
            SAKIMessageType.IMPORT_KEY -> importKey(message)
            SAKIMessageType.GENERATE_KEY -> generateKey(message)
            SAKIMessageType.GET_ENTRY -> getEntry(message)
            SAKIMessageType.LIST_KEYS -> listKeys(message)
            else -> throw Exception("Unknown request type: $message.messageType")
        }
    }

    @SuppressLint("WrongConstant")
    fun generateKey(message: SAKIMessage): SAKIMessage {
        val obj = Json.decodeFromString<AlgorithmSpecMessage>(message.data)
        val keyPairGenerator = KeyPairGenerator.getInstance(obj.algorithm, "AndroidKeyStore")

        keyPairGenerator.initialize(
            KeyGenParameterSpec.Builder(obj.keyAlias, obj.purposes)
                .setKeySize(obj.keySize)
                .setDigests(*obj.digests.toTypedArray())
                .setEncryptionPaddings(*obj.encryptionPaddings.toTypedArray())
                .build()
        )

        val keyPair = keyPairGenerator.generateKeyPair()
        val encoder = Base64.getEncoder()
        val inner = GenerateKeyResult(encoder.encodeToString(keyPair.public.encoded))
        return SAKIMessage(message.id, SAKIMessageType.GENERATE_KEY_RESULT, Json.encodeToString(inner))
    }

    fun getEntry(message: SAKIMessage): SAKIMessage {
        val obj = Json.decodeFromString<GetEntryMessage>(message.data)

        val keyStore = KeyStore.getInstance("AndroidKeyStore")
        keyStore.load(null)

        val publicKey = keyStore.getCertificate(obj.keyAlias)

        val encoder = Base64.getEncoder()
        val attributes = keyStore.getEntry(obj.keyAlias, null).attributes.map { Pair<String, String>(it.name, it.value) }
        val inner = GetEntryResult(encoder.encodeToString(publicKey.encoded), attributes)
        return SAKIMessage(message.id, SAKIMessageType.GET_ENTRY_RESULT, Json.encodeToString(inner))
    }

    @SuppressLint("WrongConstant")
    fun importKey(message: SAKIMessage): SAKIMessage {
        val obj = Json.decodeFromString<ImportKeyMessage>(message.data)
        val decoder = Base64.getDecoder()
        val decodedBytes = decoder.decode(obj.wrappedKey)

        val keyStore = KeyStore.getInstance("AndroidKeyStore")
        keyStore.load(null, null)

        val spec = KeyGenParameterSpec.Builder(
            obj.spec.keyAlias,
            KeyProperties.PURPOSE_WRAP_KEY
        )
            .setKeySize(obj.spec.keySize)
            .setDigests(*obj.spec.digests.toTypedArray())
            .setEncryptionPaddings(*obj.spec.encryptionPaddings.toTypedArray())
            .build()

        val wrappedKeyEntry = WrappedKeyEntry(decodedBytes, obj.spec.keyAlias, obj.transformation, spec)
        keyStore.setEntry(obj.wrappedKeyAlias, wrappedKeyEntry, null)

        return SAKIMessage(message.id, SAKIMessageType.IMPORT_KEY_RESULT, Json.encodeToString(ImportKeyResult(true)))
    }

    fun listKeys(message: SAKIMessage): SAKIMessage {
        val keyStore = KeyStore.getInstance("AndroidKeyStore")
        keyStore.load(null)

        return SAKIMessage(message.id, SAKIMessageType.LIST_KEYS_RESULT, Json.encodeToString(ListKeysResult(keyStore.aliases().toList())))
    }
}