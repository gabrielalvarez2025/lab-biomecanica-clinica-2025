import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random


def main_balance():
    st.set_page_config(layout="centered", initial_sidebar_state="expanded")
    st.title("Balance y control postural")

    seccion_intro = "Introducción al sistema sensoriomotor"
    seccion_estabilidad = "Concepto de estabilidad"
    seccion_propiocepcion = "La propiocepción"
    seccion_ev_clinica = "Evaluación clínica del balance"
    seccion_ev_instrumentada = "Evaluación instrumentada del balance"
    
    
    sub_seccion = st.sidebar.radio("¿Qué te gustaría aprender?", [
        seccion_intro,
        seccion_estabilidad,
        seccion_propiocepcion,
        seccion_ev_clinica,
        seccion_ev_instrumentada
    ])

    #if sub_seccion == seccion_intro:


    