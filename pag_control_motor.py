import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment


def main_control_motor():
    
    
    st.header("Unidad 3: Teorías del control motor")

    st.markdown(
        "- Teorías antiguas\n"
        "- Teoría de sistemas dinámicos\n"
        "- Teoría de modelos internos")
    
    st.title("Visualización de onda de audio")

    st.markdown("---")

    # Configuración de estilo Seaborn
sns.set_style("dark")
plt.rcParams.update({
    "axes.facecolor": "none",   # Fondo transparente
    "figure.facecolor": "none", # Fondo transparente
    "axes.edgecolor": "white",
    "axes.labelcolor": "white",
    "xtick.color": "white",
    "ytick.color": "white",
    "text.color": "white",
})

    # Subir archivo MP3
    uploaded_file = st.file_uploader("📂 Sube un archivo MP3", type=["mp3"])

    if uploaded_file is not None:
        # Cargar el audio
        audio = AudioSegment.from_file(uploaded_file, format="mp3")
        
        # Convertir a muestras numpy
        samples = np.array(audio.get_array_of_samples())
        
        # Si es estéreo, tomar solo un canal
        if audio.channels == 2:
            samples = samples[::2]
        
        # Crear eje de tiempo
        time = np.linspace(0, len(samples) / audio.frame_rate, num=len(samples))

        # Reproductor en Streamlit
        st.audio(uploaded_file, format="audio/mp3")

        # Graficar con seaborn (más bajo)
        fig, ax = plt.subplots(figsize=(12, 1.8))  # 👈 bajo y alargado
        sns.lineplot(x=time, y=samples, ax=ax, color="cyan", linewidth=1)

        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.set_title("Forma de onda del audio")

        # Fondo transparente
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        st.pyplot(fig)