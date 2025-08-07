import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

PASTEL_COLORES = ["#AEC6CF", "#FFB347", "#77DD77"]  # azul pastel, naranja pastel, verde pastel

def obtener_acc_desde_phyphox(ip: str) -> pd.DataFrame:
    url = f"http://{ip}/get?accX&accY&accZ"
    try:
        response = requests.get(url, timeout=3)
        data = response.json()

        accX = data['buffer']['accX']['buffer']
        accY = data['buffer']['accY']['buffer']
        accZ = data['buffer']['accZ']['buffer']

        # Si no hay datos, devolver DataFrame vacío
        if not accX or not accY or not accZ:
            return pd.DataFrame()

        tiempo = list(range(len(accX)))  # índice artificial para tiempo

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


def mostrar():
    st.title("Unidad 5: Análisis de marcha")
    play_acc_phyphox()
