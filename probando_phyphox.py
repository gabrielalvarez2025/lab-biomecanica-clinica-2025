import streamlit as st
import pandas as pd
import requests
from io import StringIO


def main_phyphox_transmission():
    st.title("Descargar CSV desde Acelerómetro")

    # Entrada para IP
    ip_address = st.text_input("Introduce la IP del dispositivo", "192.168.1.119")

    if st.button("Descargar y mostrar CSV"):
        try:
            # URL de exportación en formato CSV (ajusta si la ruta es diferente)
            url = f"http://{ip_address}:8080/export?format=csv"
            st.write(f"Conectando a: {url}")
            
            r = requests.get(url, timeout=5)
            r.raise_for_status()
            
            # Leer CSV en DataFrame
            csv_data = StringIO(r.text)
            df = pd.read_csv(csv_data)
            
            # Mostrar tabla
            st.write(df)
            
            # Botón para descargarlo
            st.download_button(
                label="Guardar CSV",
                data=r.content,
                file_name="acelerometro.csv",
                mime="text/csv"
            )
        except Exception as e:
            st.error(f"Error al descargar el CSV: {e}")
