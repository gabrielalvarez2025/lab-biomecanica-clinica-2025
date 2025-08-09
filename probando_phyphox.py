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


def main_phyphox():
    st.title("Unidad 5: Análisis de marcha")
    play_acc_phyphox()

