import streamlit as st
import requests
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

def main_phyphox():

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
                    valores.append(buffer[0])
                else:
                    valores.append(None)
            return valores
        except Exception as e:
            return [None] * len(CHANNELS)

    st.title("Acelerómetro en tiempo real con Phyphox")

    if 'running' not in st.session_state:
        st.session_state.running = False

    def toggle_running():
        st.session_state.running = not st.session_state.running

    boton = st.button("Iniciar / Detener lectura", on_click=toggle_running)

    texto_contenedor = st.empty()
    grafico_contenedor = st.empty()

    datos = {"Tiempo": [], "accX": [], "accY": [], "accZ": []}
    tiempo_inicio = time.time()

    while st.session_state.running:
        valores = obtener_valores()
        tiempo_actual = time.time() - tiempo_inicio

        if None not in valores:
            datos["Tiempo"].append(tiempo_actual)
            datos["accX"].append(valores[0])
            datos["accY"].append(valores[1])
            datos["accZ"].append(valores[2])

            texto_contenedor.text(f"AccX: {valores[0]:.3f} | AccY: {valores[1]:.3f} | AccZ: {valores[2]:.3f}")

            df = pd.DataFrame(datos)
            df_melt = df.melt(id_vars=["Tiempo"], value_vars=["accX", "accY", "accZ"], var_name="Eje", value_name="Valor")

            fig, ax = plt.subplots(figsize=(10, 5))
            sns.lineplot(data=df_melt, x="Tiempo", y="Valor", hue="Eje", ax=ax)
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel("Aceleración")
            ax.set_title("Acelerómetro en tiempo real")
            grafico_contenedor.pyplot(fig)
        else:
            texto_contenedor.text("No se recibieron datos completos.")

        time.sleep(0.2)

    if not st.session_state.running:
        st.write("La lectura está detenida. Presiona el botón para iniciar.")
