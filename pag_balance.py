import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random
import requests
import webbrowser
import streamlit.components.v1 as components





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

    
    col1, col2 = st.columns(2)

    with col1:
        if sub_seccion == seccion_propiocepcion:
            st.info("Para más información sobre propiocepción, consultar el artículo:")

    # URL del PDF
    url_paper_propiocepcion = "https://pmc.ncbi.nlm.nih.gov/articles/PMC164311/pdf/attr_37_01_0071.pdf"

    with col2:
        # Botón para abrir el PDF en nueva pestaña
        st.markdown(f'''
        <a href="{url_paper_propiocepcion}" target="_blank">
            <button style="padding:6px 12px; font-size:14px;">📄 Abrir artículo PDF</button>
        </a>
        ''', unsafe_allow_html=True)
    
    st.subheader("Propiocepción")

    st.markdown(
        """
        Proprioception predominates as the most misused term within the sensorimotor system. It has been incorrectly used synonymously and interchangeably with kinesthesia, joint position sense, somatosensation, balance, and reflexive joint stability. In Sherrington's13 original description of the “proprioceptive system,” proprioception was used to reference the afferent information arising from “proprioceptors” located in the “proprioceptive field.” The “proprioceptive field” was specifically defined as that area of the body “screened from the environment” by the surface cells, which contained receptors specially adapted for the changes occurring inside the organism independent of the “interoceptive field” (alimentary canal and viscera organs).13 In several of his writings, Sherrington13,14 declared proprioception as being used for the regulation of total posture (postural equilibrium) and segmental posture (joint stability), as well as initiating several conscious peripheral sensations (“muscle senses”). Although he considered vestibular information to be proprioceptive with respect to the head, Sherrington13 clearly delineated the functions of labyrinth from those receptors in the periphery. According to Matthews,15 Sherrington described 4 submodalities of “muscle sense” in Schafer's Textbook of Physiology: (1) posture, (2) passive movement, (3) active movement, and (4) resistance to movement. These submodality sensations correspond to the contemporary terms joint position sense (posture of segment), kinesthesia (active and passive), and the sense of resistance or heaviness. Thus, proprioception correctly describes afferent information arising from internal peripheral areas of the body that contribute to postural control, joint stability, and several conscious sensations.

        In contrast to proprioception, the term somatosensory (or somatosensation) is more global and encompasses all of the mechanoreceptive, thermoreceptive, and pain information arising from the periphery.2 Conscious appreciation of somatosensory information leads to the sensations of pain, temperature, tactile (ie, touch, pressure, etc), and the conscious submodality proprioception sensations. Thus, as Figure 2 illustrates, conscious appreciation of proprioception is a subcomponent of somatosensation and, therefore, the terms should not be used interchangeably.
        """
    )
