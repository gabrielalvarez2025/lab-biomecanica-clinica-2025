import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import json
import time

PASTEL_COLORES = ["#AEC6CF", "#FFB347", "#77DD77"]  # azul pastel, naranja pastel, verde pastel

def obtener_acc_desde_phyphox(ip: str, timeout=5):
    url = f"http://{ip}/get?accX&accY&accZ"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        accX = data['buffer']['accX']['buffer']
        accY = data['buffer']['accY']['buffer']
        accZ = data['buffer']['accZ']['buffer']

        # Si no tienes timestamps, usar índice
        tiempo = list(range(len(accX)))

        df = pd.DataFrame({
            "Tiempo": tiempo,
            "AccX": accX,
            "AccY": accY,
            "AccZ": accZ
        })
        return df
    except Exception as e:
        st.error(f"Error al obtener datos: {e}")
        return pd.DataFrame()

def play_acc_phyphox():
    st.header("🔄 Acelerómetro en vivo desde Phyphox")

    ip = st.text_input("IP de tu celular (sin http://)", value="192.168.1.119:8080")

    if st.button("📡 Iniciar"):
        contenedor_grafico = st.empty()
        df_acumulado = pd.DataFrame(columns=["Tiempo", "AccX", "AccY", "AccZ"])

        while True:
            df = obtener_acc_desde_phyphox(ip)
            if not df.empty:
                # Tomamos solo la última fila recibida
                ultima_fila = df.iloc[[-1]]
                df_acumulado = pd.concat([df_acumulado, ultima_fila], ignore_index=True)

                # Graficar
                df_melt = df_acumulado.melt(id_vars=["Tiempo"], var_name="Eje", value_name="Aceleración")
                fig, ax = plt.subplots(figsize=(10, 5))
                sns.lineplot(data=df_melt, x="Tiempo", y="Aceleración", hue="Eje", palette=PASTEL_COLORES, ax=ax)
                ax.set_title("Aceleración en Ejes X, Y, Z")
                contenedor_grafico.pyplot(fig)

            time.sleep(0.2)  # Actualización cada 200 ms



# Replace with the actual URL from your Phyphox app



def get_phyphox_data():
    try:
        # Construct the URL to get data from all available outputs
        # For specific outputs, you can add parameters like ?x=accelerationX&y=accelerationY

        phyphox_url = "http://192.168.1.119:8080" # Example URL
        response = requests.get(f"{phyphox_url}/get?")
        response.raise_for_status() # Raise an exception for HTTP errors
        data = response.json()
        return data
    except requests.exceptions.RequestException as e:
        print(f"Error fetching data: {e}")
        return None

def probando2():
    print("Connecting to Phyphox...")
    while True:
        sensor_data = get_phyphox_data()
        if sensor_data:
            print("--- Phyphox Data ---")
            # You can iterate through the 'buffer' or 'value' keys
            # based on the type of data you are collecting
            if 'buffer' in sensor_data:
                for key, values in sensor_data['buffer'].items():
                    print(f"{key}: {values}")
            elif 'value' in sensor_data:
                for key, value in sensor_data['value'].items():
                    print(f"{key}: {value}")
            else:
                print("No recognizable data format (buffer or value) found.")
        time.sleep(1) # Wait for 1 second before fetching new data





PP_ADDRESS = "http://192.168.1.119:8080"
CHANNELS = ["accX", "accY", "accZ"]


def main_phyphox():
    st.title("Acelerómetro en tiempo real desde Phyphox")

    ip = st.text_input("IP de tu celular (sin http://)", value="192.168.1.119:8080")

    if st.button("Iniciar lectura"):
        contenedor_texto = st.empty()
        contenedor_grafico = st.empty()

        datos_acumulados = {"Tiempo": [], "accX": [], "accY": [], "accZ": []}
        tiempo_inicial = time.time()

        while True:
            valores = obtener_valores()
            ahora = time.time() - tiempo_inicial

            if None not in valores:
                datos_acumulados["Tiempo"].append(ahora)
                datos_acumulados["accX"].append(valores[0])
                datos_acumulados["accY"].append(valores[1])
                datos_acumulados["accZ"].append(valores[2])

                contenedor_texto.text(f"AccX: {valores[0]:.3f} | AccY: {valores[1]:.3f} | AccZ: {valores[2]:.3f}")

                df = pd.DataFrame(datos_acumulados)
                df_melt = df.melt(id_vars=["Tiempo"], value_vars=["accX", "accY", "accZ"], var_name="Eje", value_name="Valor")

                fig, ax = plt.subplots(figsize=(10, 5))
                sns.lineplot(data=df_melt, x="Tiempo", y="Valor", hue="Eje", ax=ax)
                ax.set_title("Acelerómetro en tiempo real")
                ax.set_xlabel("Tiempo (s)")
                ax.set_ylabel("Aceleración")

                contenedor_grafico.pyplot(fig)
            else:
                contenedor_texto.text("No se recibieron datos completos.")

            time.sleep(0.2)


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
                valores.append(buffer[-1])
            else:
                valores.append(None)
        return valores
    except Exception as e:
        return [None] * len(CHANNELS)

