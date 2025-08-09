import streamlit as st
import requests
import time
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import subprocess

def main_phyphox2():



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
        except Exception:
            return [None] * len(CHANNELS)

    st.title("Acelerómetro en tiempo real (solo texto)")

    if 'running' not in st.session_state:
        st.session_state.running = False

    def toggle_running():
        st.session_state.running = not st.session_state.running

    boton = st.button("Iniciar / Detener lectura", on_click=toggle_running)

    contenedor = st.empty()

    while st.session_state.running:
        valores = obtener_valores()
        if None not in valores:
            texto = f"AccX: {valores[0]:.3f} | AccY: {valores[1]:.3f} | AccZ: {valores[2]:.3f}"
        else:
            texto = "No se recibieron datos completos."
        contenedor.text(texto)
        time.sleep(0.2)

    if not st.session_state.running:
        st.write("La lectura está detenida. Presiona el botón para iniciar.")

def main_phyphox():
    
    if st.button("Abrir juego Pygame"):
        subprocess.Popen(["python", "pygame_acc.py"])
        st.write("Juego abierto en una ventana nueva.")