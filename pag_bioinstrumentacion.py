import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random
import streamlit.components.v1 as components

from probando_phyphox import main_phyphox_transmission
import play_emg_sumatoria.emg_sumatoria as play_emg_sumatoria



def play_2():
    st.markdown("### Palancas y torques")
    st.markdown("""
                En esta sección exploraremos el concepto de palancas y torques, fundamentales para entender cómo se generan los movimientos en el cuerpo humano.
                """)
    st.markdown("Puedes interactuar con la simulación de palancas y torques en la barra lateral.")
    st.markdown("---")
    st.markdown("fin play 2")


def main_bioinstrumentacion():
    
    

    st.header("Unidad 1: Bioinstrumentación")

    st.markdown(
        "- Electromiografía (EMG)\n"
        "- Plataforma de fuerza\n"
        "- Videofotogrametría\n"
        "- Goniometría"
    )


    # Configuración tema seaborn
    sns.set_theme(style="darkgrid", palette="pastel")

    
    # Fin listado de contenidos
    st.markdown("---")
    # Inicio de elementos interactivos

    # Inicialización segura SOLO una vez (para botones que usan session_state)
    if "mostrar_torques" not in st.session_state:
        st.session_state["mostrar_torques"] = False
    
    if "mostrar_sumatoria" not in st.session_state:
        st.session_state["mostrar_sumatoria"] = False
    



    
    

    # Presentar botones tarjeta
    presentar_botones_tarjeta()
    
    # Tarjeta 1: Sumatoria de PAUMs
    parrafo_sumatoria = "Si tienes dudas de por qué la señal de EMG tiene la forma que tiene o cuál es su relación con los potenciales de acción de unidades motoras <b>(PAUMs)</b>, esta simulación te ayudará a entenderlo."
    botones_tarjeta(nombre_estado="mostrar_sumatoria",
                    texto_boton="Sumatoria de ondas",
                    texto_parrafo=parrafo_sumatoria,
                    color_boton= "#368581",
                    color_parrafo= "#89BBB8"
                    )
    
    # Tarjeta 2
    parrafo_interactivo2 = "Manos en la masa"
    botones_tarjeta(nombre_estado="mostrar_torques",
                    texto_boton="Procesamiento con PhyPhox",
                    texto_parrafo=parrafo_interactivo2,
                    color_boton= "#81B238",
                    color_parrafo= "#95E082"
                    )
    
    

    # ✅ Mostrar contenido si fue activado
    if st.session_state["mostrar_sumatoria"]:
        play_emg_sumatoria()
    
    if st.session_state["mostrar_torques"]:
        main_phyphox_transmission()

    st.markdown("---")


def presentar_botones_tarjeta():
    st.markdown("### **Elementos interactivos**")
    st.markdown("""
                En esta sección encontrarás elementos interactivos que te ayudarán a comprender mejor algunos de los conceptos relacionados a bioinstrumentación que vimos en clases.

                Presiona uno de los botones a continuación para activar el elemento interactivo que te interese revisar. Al presionar el botón una vez, se desplegará el elemento interactivo. Presiona nuevamente el botón para ocultarlo.
                """)
    st.empty()


def botones_tarjeta(nombre_estado, color_boton, color_parrafo, texto_boton, texto_parrafo):
    col1, col2 = st.columns([0.30, 0.70])

    with col1:
        altura_boton = 20
        font_size = 16

        color_fondo_base = color_boton
        color_fondo_hover = "#FFFFFF"
        color_fondo_active = "#0C8C1F"
        color_fuente_hover = "#2A2727"
        color_fuente_active = "#FFFFFF"
        color_fuente_parrafo = color_parrafo

        # CSS personalizado
        st.markdown(f"""
            <style>
                .big-button-container {{
                    display: flex;
                    align-items: stretch;
                    justify-content: center;
                    height: {altura_boton}px;
                    
                }}
                .big-button-container > div {{
                    width: 100%;
                }}
                div.stButton > button {{
                    width: 100%;
                    height: 100%;
                    min-height: {altura_boton}px;
                    border: 2px solid {color_fondo_base};
                    color: white;
                    background-color: {color_fondo_base};
                    font-weight: bold;
                    font-size: {font_size}px;
                    padding: 20px;
                    transition: 0.3s;
                }}
                div.stButton > button:hover {{
                    background-color: {color_fondo_hover};
                    border-color: {color_fondo_hover};
                    color: {color_fuente_hover};
                    cursor: pointer;
                }}
                div.stButton > button:active {{
                    background-color: {color_fondo_active};
                    color: {color_fuente_active};
                    border-color: {color_fondo_active};
                }}
            </style>
        """, unsafe_allow_html=True)

        if st.button(texto_boton, use_container_width=True):
            st.session_state[nombre_estado] = not st.session_state[nombre_estado]

    with col2:
        st.markdown(f"""
            <p style="font-size: 16px; margin-top: 10px; color: {color_fuente_parrafo};">
            {texto_parrafo}
            </p>
        """, unsafe_allow_html=True)
