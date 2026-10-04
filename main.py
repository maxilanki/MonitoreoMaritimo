import json
import websocket

API_KEY = "be1188d428a6d284283b8bd8f3d8baedc36cb509"

def on_message(ws, message):
    try:
        data = json.loads(message)
        msg_type = data.get("MessageType")
        
        # Confirmación de que estamos recibiendo cualquier tipo de datos
        meta = data.get("MetaData", {})
        nombre = meta.get("ShipName", "Desconocido").strip()
        mmsi = meta.get("MMSI", "N/A")
        
        if msg_type == "PositionReport":
            pos = data["Message"]["PositionReport"]
            print(f"🚢 [POSICIÓN] {nombre} (MMSI: {mmsi})")
            print(f"   📍 Lat: {pos.get('Latitude')}, Lon: {pos.get('Longitude')}")
            print(f"   💨 Velocidad: {pos.get('Sog')} nudos | Rumbo: {pos.get('TrueHeading')}°")
            print("-" * 50)
        else:
            # Imprime otros mensajes para comprobar tráfico activo
            print(f"📡 [OTRO MENSAJE - {msg_type}] Barco: {nombre} (MMSI: {mmsi})")
            
    except Exception as e:
        print(f"⚠️ Error procesando mensaje: {e}")

def on_error(ws, error):
    print(f"❌ Error de conexión: {error}")

def on_close(ws, close_status_code, close_msg):
    print("🔌 Conexión cerrada.")

def on_open(ws):
    print("✅ Conexión establecida. Escuchando tráfico marítimo...\n")
    
    # Cuadro más amplio alrededor de la costa de Colima / Jalisco para probar
    zona_amplia_box = [[35.70, -6.10], [36.30, -5.10]]
    
    subscribe_message = {
        "APIKey": API_KEY,
        "BoundingBoxes": [zona_amplia_box]
    }
    ws.send(json.dumps(subscribe_message))

if __name__ == "__main__":
    ws = websocket.WebSocketApp(
        "wss://stream.aisstream.io/v0/stream",
        on_open=on_open,
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()