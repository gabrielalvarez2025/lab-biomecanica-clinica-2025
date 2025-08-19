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

        # Graficar
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(time, samples, color="purple")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.set_title("Forma de onda del audio")
        st.pyplot(fig)