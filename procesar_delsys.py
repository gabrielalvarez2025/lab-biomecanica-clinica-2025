import streamlit as st
import pandas as pd

uploaded_file = st.file_uploader("📂 Sube un CSV de Delsys", type="csv")

if uploaded_file is not None:
    st.success("Archivo cargado ✅")

    # Leer todo como texto, sin parseo de columnas
    raw = pd.read_csv(uploaded_file, header=None, dtype=str, engine="python")

    # Eliminar filas de metadatos (0 a 6)
    raw = raw.drop(index=range(0,7)).reset_index(drop=True)

    # Asignar fila de headers (ahora primera fila)
    raw.columns = raw.iloc[0]
    df = raw.drop(0).reset_index(drop=True)

    # Convertir comas a puntos y a float donde sea posible
    for col in df.columns:
        df[col] = df[col].str.replace(",", ".").astype(float, errors="ignore")

    st.dataframe(df)
