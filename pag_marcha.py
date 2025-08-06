import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

def obtener_acc_desde_phyphox(ip: str) -> pd.DataFrame:
    url = f"http://{ip}/get?accX&accY&accZ"
    try:
        response = requests.get(url, timeout=3)
        data = response.json()

        accX = data['buffer']['accX']['buffer']
        accY = data['buffer']['accY']['buffer']
        accZ = data['buffer']['accZ']['buffer']

        # Crear un eje de tiempo simple (índice)
        tiempo = list(range(len(accX)))

        df = pd.DataFrame({
            "Tiempo": tiempo,
            "AccX": accX,
            "AccY": accY,
            "AccZ": accZ
        })
        return df
    except Exception as e:
        print(f"Error: {e}")
        return pd.DataFrame()

PASTEL_PALETTE = sns.color_palette("pastel")

def play_acc_phyphox():
    st.subheader("🔁 Acelerómetro - Phyphox")

    ip = st.text_input("Introduce la IP del dispositivo Phyphox (ej. http://192.168.0.25:8080)", key="phyphox_ip")

    if st.button("Conectar y graficar"):
        if not ip:
            st.warning("Por favor, ingresa una IP válida.")
            return

        try:
            url = f"{ip}/get"
            response = requests.get(url, timeout=3)  # timeout para evitar espera infinita
            response.raise_for_status()

            data_json = response.json()

            if "buffer" not in data_json:
                st.error("No se encontró el buffer en la respuesta.")
                return

            acc_data = data_json["buffer"]

            # Convertir a DataFrame
            df = pd.DataFrame(acc_data)
            df = df.rename(columns={
                'accX': 'X', 'accY': 'Y', 'accZ': 'Z'
            })
            df = df.tail(100)  # últimos 100 valores

            st.write("Datos recibidos:")
            st.dataframe(df)

            # Gráfico
            plt.figure(figsize=(10, 4))
            sns.lineplot(data=df, palette=PASTEL_PALETTE)
            plt.title("Acelerómetro (últimos 100 datos)")
            plt.xlabel("Tiempo (muestras)")
            plt.ylabel("Aceleración (m/s²)")
            st.pyplot(plt.gcf())

        except requests.exceptions.RequestException as e:
            st.error(f"Error de conexión: {e}")
        except Exception as e:
            st.error(f"Otro error: {e}")

def mostrar():
    st.title("Unidad 5: Análisis de marcha")
    play_acc_phyphox()
