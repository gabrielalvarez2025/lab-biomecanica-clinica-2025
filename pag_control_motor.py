import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from pydub import AudioSegment
from pydub.utils import which

# Forzar uso de ffmpeg
AudioSegment.converter = which("ffmpeg")

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

    uploaded_file = st.file_uploader("📂 Sube un archivo MP3", type=["mp3"])

    if uploaded_file is not None:
        # Cargar MP3 con pydub
        audio = AudioSegment.from_file(uploaded_file, format="mp3")
        
        samples = np.array(audio.get_array_of_samples())
        if audio.channels == 2:
            samples = samples[::2]  # usar un canal si es estéreo
        
        time = np.linspace(0, len(samples) / audio.frame_rate, num=len(samples))

        # Reproductor
        st.audio(uploaded_file, format="audio/mp3")

        # Gráfico bajo y ancho
        fig, ax = plt.subplots(figsize=(12, 1.5))
        sns.lineplot(x=time, y=samples, ax=ax, color="cyan", linewidth=1)

        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.set_title("Forma de onda del audio")

        # Fondo transparente
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        st.pyplot(fig)
