import streamlit as st

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
        # Cargar el audio con pydub
        audio = AudioSegment.from_file(uploaded_file, format="mp3")
        
        # Convertir a array de muestras
        samples = np.array(audio.get_array_of_samples())
        
        # Si es estéreo, usar solo un canal
        if audio.channels == 2:
            samples = samples[::2]
        
        # Eje de tiempo
        time = np.linspace(0, len(samples) / audio.frame_rate, num=len(samples))

        # Mostrar reproductor en Streamlit
        st.audio(uploaded_file, format="audio/mp3")

        # Graficar onda
        fig, ax = plt.subplots(figsize=(10, 4))
        ax.plot(time, samples, color="purple")
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Amplitud")
        ax.set_title("Forma de onda del audio")
        st.pyplot(fig)