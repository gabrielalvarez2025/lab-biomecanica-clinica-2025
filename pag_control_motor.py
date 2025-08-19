import streamlit as st
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
import librosa

def main_control_motor():
    st.title("Visualización de onda de audio (MP3)")

    uploaded_file = st.file_uploader("📂 Sube un archivo MP3", type=["mp3"])

    if uploaded_file is not None:
        # Cargar audio con librosa
        y, sr = librosa.load(uploaded_file, sr=None, mono=True)

        # Eje tiempo
        time = np.linspace(0, len(y) / sr, num=len(y))

        # Reproductor
        st.audio(uploaded_file, format="audio/mp3")

        # Graficar
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

        fig, ax = plt.subplots(figsize=(12, 1.5))
        sns.lineplot(x=time, y=y, ax=ax, color="cyan", linewidth=1)

        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.set_title("Forma de onda del audio")
        fig.patch.set_alpha(0.0)
        ax.patch.set_alpha(0.0)

        st.pyplot(fig)
