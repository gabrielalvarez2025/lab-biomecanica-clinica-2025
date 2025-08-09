import streamlit as st
import pandas as pd
import requests
from io import StringIO


def main_phyphox_transmission():
    st.title("Visualización de Aceleraciones en el Tiempo")

    uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

    if uploaded_file is not None:
        # Leer CSV
        df = pd.read_csv(uploaded_file, sep="\t")  # usa tabulador como separador
        
        # Renombrar columnas si es necesario (eliminar espacios y asegurar nombres correctos)
        df.columns = df.columns.str.strip()

        st.write("Vista previa de los datos:")
        st.dataframe(df.head())

        # Configuración de Seaborn
        sns.set_theme(style="whitegrid", palette="pastel")

        # Crear la figura
        fig, ax = plt.subplots(figsize=(10, 6))

        # Graficar cada eje
        sns.lineplot(x=df["Time (s)"], y=df["Acceleration x (m/s^2)"], label="Acc X", ax=ax)
        sns.lineplot(x=df["Time (s)"], y=df["Acceleration y (m/s^2)"], label="Acc Y", ax=ax)
        sns.lineplot(x=df["Time (s)"], y=df["Acceleration z (m/s^2)"], label="Acc Z", ax=ax)

        ax.set_title("Aceleraciones en el Tiempo", fontsize=16)
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Aceleración (m/s²)")

        st.pyplot(fig)