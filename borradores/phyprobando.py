import requests
import time

PP_ADDRESS = "http://192.168.1.119:8080"
CHANNELS = ["accX", "accY", "accZ"]

def obtener_valores():
    url = PP_ADDRESS + "/get?" + "&".join(CHANNELS)
    try:
        r = requests.get(url, timeout=2)
        r.raise_for_status()
        data = r.json()
        valores = []
        for ch in CHANNELS:
            buffer = data["buffer"].get(ch, {}).get("buffer", [])
            if buffer:
                valores.append(buffer[0])  # El primer y único valor
            else:
                valores.append(None)
        return valores
    except Exception as e:
        print(f"Error al obtener datos: {e}")
        return [None]*len(CHANNELS)

if __name__ == "__main__":
    print("Leyendo acelerómetro en tiempo real. Ctrl+C para salir.")
    while True:
        ax, ay, az = obtener_valores()
        if None not in (ax, ay, az):
            print(f"AccX: {ax:.3f} | AccY: {ay:.3f} | AccZ: {az:.3f}")
        else:
            print("No se recibieron datos completos.")
        time.sleep(0.2)