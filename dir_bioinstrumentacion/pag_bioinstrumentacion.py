import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

from dir_bioinstrumentacion.play_ondas_emg import play as interactivo_sumatoria

def mostrar():
    st.header("Unidad 1: Bioinstrumentación")

    st.markdown(
        "- Electromiografía (EMG) hola\n"
        "- Plataforma de fuerza\n"
        "- Videofotogrametría\n"
        "- Goniometría"
    )

    sns.set_theme(style="darkgrid", palette="pastel")

    st.markdown("hola")

    
    
    # ELEMENTO INTERACTIVO: Descomposición de ondas
    interactivo_sumatoria()
    
    