from flask import Flask
import asyncio
import websockets

app = Flask(__name__)

ASSEMBLY_WS = "wss://streaming.assemblyai.com/v3/ws?sample_rate=16000&speech_model=u3-rt-pro"

@app.route("/")
def home():
    return "Realtime server running"

# (لاحقاً بنضيف WebSocket bridge هنا)
