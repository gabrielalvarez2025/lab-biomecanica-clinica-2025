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
        "- Goniometría"
    )

    sns.set_theme(style="darkgrid", palette="pastel")

    
    
    # ELEMENTO INTERACTIVO: Descomposición de ondas
    st.subheader("Descomposición de ondas")

    st.markdown("""
    A continuación, puedes interactuar con una herramienta que simula la descomposición de una señal electromiográfica (EMG) en varias unidades motoras (UM).
    Esta herramienta te permite simular la descomposición de una señal EMG en varias unidades motoras (UM).
    
    
    """)

    st.info("⬅ En la barra lateral están los parámetros de cada onda.")

    st.markdown("""
    **Juega con ellos** para ajustar la amplitud, frecuencia y fase de cada onda y **mira cómo van cambiando su forma**:
                
    """)

    # Parámetros de usuario
    st.sidebar.title("Parámetros de simulación")
    num_ondas = st.sidebar.slider("Número de ondas (UM)", 1, 15, 6)
    freq_max = st.sidebar.slider("Frecuencia máxima (Hz)", 10, 100, 20)
    amp_max = 2
    fase_max = np.pi * 5

    x = np.linspace(0, 2 * np.pi, 500)
    suma_total = np.zeros_like(x)
    colores_pastel = sns.color_palette("pastel", num_ondas)

    # Sliders por onda
    params = []
    for i in range(num_ondas):
        with st.sidebar.expander(f"Unidad motora {i+1}", expanded=False):
            amp = st.slider(f"Amplitud {i+1}", 0.0, float(amp_max), 1.0, key=f"amp_{i}")
            freq = st.slider(f"Frecuencia {i+1} (Hz)", 0.0, float(freq_max), 1.0, key=f"freq_{i}")
            fase = st.slider(f"Fase {i+1}", 0.0, float(fase_max), 0.0, key=f"fase_{i}")
            params.append((amp, freq, fase))

    # Primera figura: ondas individuales
    fig1, axs1 = plt.subplots(num_ondas, 1, figsize=(10, num_ondas * 1.5))

    # Fondo transparente
    fig1.patch.set_alpha(0)
    for ax in axs1:
        ax.patch.set_alpha(0)

    for i, (amp, freq, fase) in enumerate(params):
        y = amp * np.sin(2 * np.pi * freq * x + fase)
        suma_total += y
        axs1[i].plot(x, y, color=colores_pastel[i])
        axs1[i].set_ylim(-amp_max, amp_max)
        axs1[i].set_ylabel(f"UM {i+1}")
        axs1[i].set_xticks([])

    st.pyplot(fig1)

    # Segunda figura: gráfico sumatoria total
    fig2, ax2 = plt.subplots(figsize=(10, 3))

    # Fondo transparente
    fig2.patch.set_alpha(0)
    ax2.patch.set_alpha(0)

    ax2.plot(x, suma_total, color='white')
    ax2.set_ylim(-amp_max * num_ondas, amp_max * num_ondas)
    ax2.set_ylabel("Suma")
    ax2.set_xlabel("Tiempo (ms)")
    ax2.set_title("Simulación de señal EMG compuesta")

    st.pyplot(fig2)