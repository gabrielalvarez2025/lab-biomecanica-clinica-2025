import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns

def obtener_acc_desde_phyphox(ip: str) -> pd.DataFrame:
    url = f"http://{ip}/get?accX&accY&accZ"
    try:
        response = requests.get(url)
        data = response.json()

        accX = data['buffer']['accX']['data']
        accY = data['buffer']['accY']['data']
        accZ = data['buffer']['accZ']['data']
        timestamps = data['buffer']['accX']['time']

        df = pd.DataFrame({
            "Tiempo (s)": timestamps,
            "AccX": accX,
            "AccY": accY,
            "AccZ": accZ
        })
        return df
    except Exception as e:
        st.error(f"❌ Error al obtener datos: {e}")
        return pd.DataFrame()

PASTEL_COLORES = ["#AEC6CF", "#FFB347", "#77DD77"]

def play_acc_phyphox():
    st.subheader("🔄 Acelerómetro en tiempo real desde Phyphox")

    ip = st.text_input("📱 IP de tu celular (sin 'http://')", value="192.168.1.5:8080")

    if st.button("📡 Obtener datos"):
        df = obtener_acc_desde_phyphox(ip)

        if df.empty:
            st.warning("⚠ No se pudieron obtener datos. Revisa la IP o que el experimento esté corriendo.")
        else:
            st.success("✅ Datos recibidos correctamente.")

            # Formatear y graficar
            df_melt = df.melt(id_vars=["Tiempo (s)"], var_name="Eje", value_name="Aceleración")

            fig, ax = plt.subplots()
            sns.lineplot(data=df_melt, x="Tiempo (s)", y="Aceleración", hue="Eje", palette=PASTEL_COLORES, ax=ax)
            ax.set_title("📊 Aceleración en Ejes X, Y, Z", fontsize=14)
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel("Aceleración (m/s²)")
            st.pyplot(fig)

def mostrar():
    st.title("Unidad 5: Análisis de marcha")
    play_acc_phyphox()
