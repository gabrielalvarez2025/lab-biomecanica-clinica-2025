import streamlit as st
import numpy as np
import librosa
import librosa.display
import matplotlib.pyplot as plt

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
        # Cargar el audio con librosa
        y, sr = librosa.load(uploaded_file, sr=None)  # sr=None = conserva la frecuencia original

        # Mostrar reproductor en Streamlit
        st.audio(uploaded_file, format="audio/mp3")

        # Graficar la onda
        fig, ax = plt.subplots(figsize=(10, 4))
        librosa.display.waveshow(y, sr=sr, ax=ax, color="purple")
        ax.set_title("Forma de onda del audio")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        st.pyplot(fig)