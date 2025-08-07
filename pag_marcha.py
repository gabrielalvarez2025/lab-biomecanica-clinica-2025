import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

PASTEL_COLORES = ["#AEC6CF", "#FFB347", "#77DD77"]  # azul pastel, naranja pastel, verde pastel

def obtener_acc_desde_phyphox(ip: str, timeout=10):
    url = f"http://{ip}/get?accX&accY&accZ"
    try:
        response = requests.get(url, timeout=timeout)
        response.raise_for_status()
        data = response.json()

        accX = data['buffer']['accX']['buffer']
        accY = data['buffer']['accY']['buffer']
        accZ = data['buffer']['accZ']['buffer']
        timestamps = data['buffer']['accX'].get('time', list(range(len(accX))))  # si no hay 'time', usa índice

        df = pd.DataFrame({
            "Tiempo (s)": timestamps,
            "AccX": accX,
            "AccY": accY,
            "AccZ": accZ
        })
        return df
    except requests.exceptions.ConnectTimeout:
        print(f"Timeout: No se pudo conectar a {ip} en {timeout} segundos")
    except requests.exceptions.ConnectionError as e:
        print(f"Error de conexión: {e}")
    except Exception as e:
        print(f"Error inesperado: {e}")
    return pd.DataFrame()

def play_acc_phyphox():
    st.header("🔄 Acelerómetro desde Phyphox")

    ip = st.text_input("Ingresa la IP de tu celular (sin http://)", value="192.168.1.5:8080")

    if st.button("📡 Obtener datos"):
        df = obtener_acc_desde_phyphox(ip)

        if df.empty:
            st.warning("No se pudieron obtener datos. Verifica la IP y que Phyphox esté corriendo.")
        else:
            st.success("Datos recibidos correctamente 🎉")

            df_melt = df.melt(id_vars=["Tiempo"], var_name="Eje", value_name="Aceleración")

            fig, ax = plt.subplots(figsize=(10, 5))
            sns.lineplot(data=df_melt, x="Tiempo", y="Aceleración", hue="Eje", palette=PASTEL_COLORES, ax=ax)
            ax.set_title("Aceleración en Ejes X, Y, Z")
            st.pyplot(fig)


#def mostrar():
st.title("Unidad 5: Análisis de marcha")
print('conexion ok con terminal')
play_acc_phyphox()

