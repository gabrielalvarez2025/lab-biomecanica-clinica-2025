import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

def mostrar():
    
    
    st.header("Unidad 1: Bioinstrumentación")

    st.markdown(
        "- Electromiografía (EMG)\n"
        "- Plataforma de fuerza\n"
        "- Videofotogrametría\n"
        "- Goniometría")
    
    # archivo: streamlit_emg_sim.py

    # Configuración
    st.set_page_config(layout="wide")
    sns.set_theme(style="darkgrid", palette="pastel")

    # Parámetros de usuario
    st.sidebar.title("Parámetros de simulación")
    num_ondas = st.sidebar.slider("Número de ondas (UM)", 1, 15, 6)
    freq_max = st.sidebar.slider("Frecuencia máxima (Hz)", 10, 100, 20)
    amp_max = 2
    fase_max = np.pi * 5

    # Variables
    x = np.linspace(0, 2 * np.pi, 500)
    suma_total = np.zeros_like(x)
    colores_pastel = sns.color_palette("pastel", num_ondas)

    # Sliders por onda
    params = []
    for i in range(num_ondas):
        with st.sidebar.expander(f"Unidad motora {i+1}", expanded=False):
            amp = st.slider(f"Amplitud {i+1}", 0.0, amp_max, 1.0, key=f"amp_{i}")
            freq = st.slider(f"Frecuencia {i+1} (Hz)", 0.0, float(freq_max), 1.0, key=f"freq_{i}")
            fase = st.slider(f"Fase {i+1}", 0.0, float(fase_max), 0.0, key=f"fase_{i}")
            params.append((amp, freq, fase))

    # Gráfico principal
    fig, axs = plt.subplots(num_ondas + 1, 1, figsize=(10, num_ondas * 1.5))
    for i, (amp, freq, fase) in enumerate(params):
        y = amp * np.sin(2 * np.pi * freq * x + fase)
        suma_total += y
        axs[i].plot(x, y, color=colores_pastel[i])
        axs[i].set_ylim(-amp_max, amp_max)
        axs[i].set_ylabel(f"UM {i+1}")
        axs[i].set_xticks([])

    # Onda sumatoria
    axs[-1].plot(x, suma_total, color='k')
    axs[-1].set_ylim(-amp_max*num_ondas, amp_max*num_ondas)
    axs[-1].set_ylabel("Suma")
    axs[-1].set_xlabel("Tiempo (ms)")
    axs[-1].set_title("Composición de señales EMG")

    st.pyplot(fig)
