import json
import threading
import websocket
from flask import Flask, render_template
from flask_socketio import SocketIO

app = Flask(__name__, template_folder='.')
socketio = SocketIO(app, cors_allowed_origins="*")

# TU API KEY DE AISSTREAM SE QUEDA AQUÍ EN EL BACKEND
API_KEY = "be1188d428a6d284283b8bd8f3d8baedc36cb509"

def on_message(ws, message):
    try:
        data = json.loads(message)
        msg_type = data.get("MessageType")
        
        if msg_type == "PositionReport":
            pos = data["Message"]["PositionReport"]
            meta = data["MetaData"]
            
            barco_data = {
                "mmsi": meta.get("MMSI"),
                "name": meta.get("ShipName", "Desconocido").strip(),
                "lat": pos.get("Latitude"),
                "lng": pos.get("Longitude"),
                "sog": pos.get("Sog"),
                "heading": pos.get("TrueHeading")
            }
            
            # Reenviar el barco capturado al navegador web
            socketio.emit('vessel_update', barco_data)
            print(f"🚢 Barco enviado al mapa: {barco_data['name']} ({barco_data['mmsi']})")
            
    except Exception as e:
        print(f"Error procesando mensaje: {e}")

def run_ais_listener():
    def on_open(ws):
        print("✅ Conectado a AISStream. Escuchando Manzanillo...")
        cobertura_manzanillo = [[18.9000, -104.6500], [19.3000, -104.1000]]
        subscribe_message = {
            "APIKey": API_KEY,
            "BoundingBoxes": [cobertura_manzanillo]
        }
        ws.send(json.dumps(subscribe_message))

    ws = websocket.WebSocketApp(
        "wss://stream.aisstream.io/v0/stream",
        on_open=on_open,
        on_message=on_message
    )
    ws.run_forever()

# Iniciar la escucha de la API en segundo plano
threading.Thread(target=run_ais_listener, daemon=True).start()

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    print("🚀 Servidor iniciado en http://localhost:5000")
    socketio.run(app, port=5000)