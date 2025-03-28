package com.bobani.saki

import android.app.Service
import android.content.Intent
import android.os.IBinder
import android.util.Log
import okhttp3.WebSocket
import okhttp3.OkHttpClient
import okhttp3.Request

class SAKIListenerService: Service() {
    var websocketListener: SAKIWebSocketListener? = null
    var webSocket: WebSocket? = null
    var client: OkHttpClient? = null


    override fun onCreate() {
        websocketListener = SAKIWebSocketListener()
        client = OkHttpClient()
        webSocket = client?.newWebSocket(Request.Builder().url("ws://172.21.57.157:8765/").build(), websocketListener!!)
        Log.d("WS LISTENER", "BOOTING UP!")
    }

    override fun onBind(intent: Intent?): IBinder? {
        return null
    }
}