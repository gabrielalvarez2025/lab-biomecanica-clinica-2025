import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

from dir_bioinstrumentacion.play_ondas_emg import play as interactivo_sumatoria

def mostrar():
    st.header("Unidad 1: Bioinstrumentación")

    st.markdown(
        "- Electromiografía (EMG)\n"
        "- Plataforma de fuerza\n"
        "- Videofotogrametría\n"
        "- Goniometría"
    )

    sns.set_theme(style="darkgrid", palette="pastel")

    st.markdown("hola")

    
    
    # ELEMENTO INTERACTIVO: Descomposición de ondas
    #interactivo_sumatoria()

    # Estilo CSS personalizado para los botones tipo tarjeta
    card_style = """
    <style>
    .card {
        background-color: #1f1f1f;
        padding: 30px;
        border-radius: 15px;
        text-align: center;
        box-shadow: 4px 4px 10px rgba(0,0,0,0.5);
        transition: 0.3s;
        cursor: pointer;
    }
    .card:hover {
        background-color: #333333;
        transform: scale(1.02);
    }
    .card a {
        color: white;
        text-decoration: none;
        font-size: 24px;
        font-weight: bold;
    }
    </style>
    """
    st.markdown(card_style, unsafe_allow_html=True)

    # Crear columnas para mostrar los botones en horizontal
    col1, col2, col3 = st.columns(3)

    with col1:
        mensaje_boton1 = "Sumatoria de ondas"
        st.markdown(f'<div class="card"><a href="/play_ondas_emg">{mensaje_boton1}</a></div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card"><a href="/Pagina2">Ir a Página 2</a></div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="card"><a href="/Home">Volver al Inicio</a></div>', unsafe_allow_html=True)
    
    