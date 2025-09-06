import streamlit as st
import pandas as pd

def main_delsys():
    st.markdown("---")
    st.subheader("Procesando Datos EMG/IMU Delsys")

    uploaded_file = st.file_uploader("📂 Sube un archivo CSV de Delsys", type=["csv"])

    if uploaded_file is not None:
        st.success("¡Archivo CSV de Delsys cargado exitosamente! ✅")

        # ---- Leer headers (fila 6) y frecuencias (fila 7) ----
        header_row = 5   # Python index = fila 6 de Excel
        freq_row = 6     # Python index = fila 7 de Excel

        # Leemos el archivo completo con ; como separador
        raw = pd.read_csv(uploaded_file, delimiter=";", header=None)

        # Extraer headers y frecuencias
        headers = raw.iloc[header_row].tolist()
        freqs = raw.iloc[freq_row].tolist()

        # Guardar frecuencias en un dict {columna: frecuencia}
        freq_dict = {col: freq for col, freq in zip(headers, freqs)}

        # ---- Leer datos desde fila 9 (Python index = 8) ----
        df = pd.read_csv(uploaded_file, delimiter=";", skiprows=8, names=headers)

        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip()

        # ---- Mostrar resultados ----
        st.markdown("### Vista previa de tus datos:")
        st.dataframe(df.head(), hide_index=True)

        st.markdown("### Frecuencias de muestreo detectadas:")
        st.json(freq_dict)
