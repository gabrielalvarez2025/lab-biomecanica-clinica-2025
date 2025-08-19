import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from scipy.io import wavfile

def main_control_motor():
    st.header("Unidad 3: Teorías del control motor")

    st.markdown(
        "- Teorías antiguas\n"
        "- Teoría de sistemas dinámicos\n"
        "- Teoría de modelos internos")
    
    st.title("Visualización de onda de audio")
    st.markdown("---")

    # Estilo seaborn con fondo transparente y letras blancas
    sns.set_style("dark")
    plt.rcParams.update({
        "axes.facecolor": "none",
        "figure.facecolor": "none",
        "axes.edgecolor": "white",
        "axes.labelcolor": "white",
        "xtick.color": "white",
        "ytick.color": "white",
        "text.color": "white",
    })

    # Subir archivo WAV (más seguro que MP3 en tu entorno)
    uploaded_file = st.file_uploader("📂 Sube un archivo WAV", type=["mp3"])

    if uploaded_file is not None:
        # Leer archivo wav
        samplerate, samples = wavfile.read(uploaded_file)

        # Si es estéreo, tomar solo un canal
        if samples.ndim > 1:
            samples = samples[:, 0]

        # Crear eje de tiempo
        time = np.linspace(0, len(samples) / samplerate, num=len(samples))

        # Reproductor en Streamlit
        st.audio(uploaded_file, format="audio/wav")

        # Graficar
        fig, ax = plt.subplots(figsize=(12, 1.5))  # más bajo
        sns.lineplot(x=time, y=samples, ax=ax, color="cyan", linewidth=1)

        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.set_title("Forma de onda del audio")

        # Fondo transparente
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        st.pyplot(fig)
