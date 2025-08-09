import streamlit as st
import pandas as pd
import requests
from io import StringIO


def main_phyphox_transmission():
    st.title("Descargar CSV desde Acelerómetro")

    st.title("Visualizar CSV como tabla")

    uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

    if uploaded_file is not None:
        # Leer CSV
        df = pd.read_csv(uploaded_file)
        
        # Mostrar tabla
        st.write("Vista previa del CSV:")
        st.dataframe(df, use_container_width=True)