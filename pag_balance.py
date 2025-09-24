import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random
import requests



def main_balance():
    st.set_page_config(layout="centered", initial_sidebar_state="expanded")
    st.markdown("##### Sistema sensoriomotor, balance y control postural")

    seccion_intro = "El sistema sensoriomotor"
    seccion_estabilidad = "Concepto de estabilidad"
    seccion_propiocepcion = "La propiocepción"
    seccion_ev_clinica = "Evaluación clínica del balance"
    seccion_ev_instrumentada = "Evaluación instrumentada"
    
    
    sub_seccion = st.sidebar.radio("¿Qué te gustaría aprender?", [
        seccion_intro,
        seccion_estabilidad,
        seccion_propiocepcion,
        seccion_ev_clinica,
        seccion_ev_instrumentada
    ])

    if sub_seccion == seccion_propiocepcion:
        st.info("Para más infromación sobre propiocepción, consultar el artículo: ")

    # URL del PDF
    url_paper_propiocepcion = "https://pmc.ncbi.nlm.nih.gov/articles/PMC164311/pdf/attr_37_01_0071.pdf"

    # Descargar el PDF en memoria
    response = requests.get(url_paper_propiocepcion)
    pdf_bytes = response.content

    # Crear botón de descarga
    st.download_button(
        label="📄 Descargar artículo PDF",
        data=pdf_bytes,
        file_name="articulo.pdf",
        mime="application/pdf"
    )