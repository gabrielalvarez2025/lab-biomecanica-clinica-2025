import streamlit as st
import pandas as pd

def main_delsys():
    st.markdown("---")
    st.subheader("Procesando Datos EMG/IMU Delsys")

    uploaded_file = st.file_uploader("📂 Sube un archivo CSV de Delsys", type=["csv"])

    if uploaded_file is not None:
        st.success("¡Archivo CSV de Delsys cargado exitosamente! ✅")

        # --- Leemos TODO el archivo con delimitador ; sin asumir cabeceras ---
        raw = pd.read_csv(
            uploaded_file,
            delimiter=";",
            header=None,
            engine="python",
            on_bad_lines="skip"   # ignora filas con columnas inconsistentes
        )

        # Extraer headers (fila 6 -> index 5 en pandas)
        headers = raw.iloc[5].fillna("").tolist()

        # Extraer frecuencias (fila 7 -> index 6 en pandas)
        freqs = raw.iloc[6].fillna("").tolist()
        freq_dict = {col: freq for col, freq in zip(headers, freqs)}

        # Extraer datos desde fila 9 en adelante (index 8)
        df = pd.read_csv(
            uploaded_file,
            delimiter=";",
            skiprows=8,
            names=headers,
            engine="python",
            on_bad_lines="skip"
        )

        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip()

        # --- Mostrar vista previa ---
        st.markdown("### Vista previa de tus datos:")
        st.dataframe(df.head(), hide_index=True)

        st.markdown("### Frecuencias de muestreo detectadas:")
        st.json(freq_dict)
