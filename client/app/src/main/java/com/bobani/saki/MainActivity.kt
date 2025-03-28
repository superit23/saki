package com.bobani.saki

import android.content.Intent
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.Spacer
import androidx.compose.foundation.layout.fillMaxHeight
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.layout.size
import androidx.compose.ui.unit.dp
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Scaffold
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.MutableState
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.ui.Modifier
import androidx.compose.ui.tooling.preview.Preview
import com.bobani.saki.ui.theme.SAKITheme
import androidx.compose.runtime.getValue
import androidx.compose.runtime.setValue
import androidx.compose.ui.text.style.TextAlign
import okhttp3.OkHttpClient
import okhttp3.Request
import okhttp3.WebSocket

class MainActivity : ComponentActivity() {
    var webSocket: WebSocket? = null

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
//        startService(Intent(this, SAKIListenerService::class.java))

        val websocketListener = SAKIWebSocketListener()
        val client = OkHttpClient()
        webSocket = client.newWebSocket(Request.Builder().url("ws://172.21.57.157:8765/").build(), websocketListener!!)

        enableEdgeToEdge()
        setContent {
            SAKITheme {
                Scaffold(modifier = Modifier.fillMaxSize()) { innerPadding ->
                    URLField(
                        modifier = Modifier.padding(innerPadding)
                    )
                }
            }
        }
    }
}

@Composable
fun URLField(modifier: Modifier = Modifier) {
    Column(
    ) {
        Row(Modifier.size(width = 100.dp, height = 20.dp)) {
            var url by remember {
                mutableStateOf("hiya")
            }
            Text("URL", modifier=modifier.fillMaxHeight())
            Spacer(modifier=modifier
                .padding(horizontal = 10.dp))
            OutlinedTextField(
                value = url,
                onValueChange = { text: String ->
                    url = text
                },
                modifier = modifier
            )
        }
        }


}

@Preview(showBackground = true)
@Composable
fun GreetingPreview() {
    SAKITheme {
        URLField()
    }
}