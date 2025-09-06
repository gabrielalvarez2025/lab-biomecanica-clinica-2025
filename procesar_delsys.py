import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main_delsys():
    st.markdown("---")
    st.subheader("Procesando Datos EMG/IMU Delsys")

    uploaded_file = st.file_uploader("📂 Sube un archivo CSV de Delsys", type=["csv"])

    if uploaded_file is not None:
        st.success("¡Archivo CSV de Delsys cargado exitosamente! ✅")

        # Leer todo sin asignar headers todavía
        raw = pd.read_csv(uploaded_file, header=None, dtype=str)

        # Detectar automáticamente la fila de headers
        header_row_idx = raw[raw.apply(lambda row: row.str.contains("ACC X Time Series", na=False)).any(axis=1)].index[0]
        headers = raw.iloc[header_row_idx].str.strip()

        # Guardar filas previas como metadatos (opcional)
        metadatos = raw.iloc[:header_row_idx]

        # Tomar los datos debajo del header
        df = raw.iloc[header_row_idx + 1:].copy()
        df.columns = headers
        df = df.reset_index(drop=True)

        # Convertir columnas numéricas a float (reemplazando ',' por '.')
        for col in df.columns:
            try:
                df[col] = df[col].str.replace(",", ".").astype(float)
            except:
                pass  # columnas que no se pueden convertir se mantienen

        st.markdown("### Metadatos:")
        st.dataframe(metadatos, hide_index=True)

        st.markdown("### Vista previa de tus datos:")
        st.dataframe(df, hide_index=True)
