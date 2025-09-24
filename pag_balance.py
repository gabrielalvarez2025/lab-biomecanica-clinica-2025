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

    tab1, tab2, tab3, tab4, tab5 = st.tabs([
        "Propiocepción",
        "Somatosensación"
    ])

    
    st.markdown(
        """
        Proprioception predominates as the most misused term within the sensorimotor system. It has been incorrectly used synonymously and interchangeably with kinesthesia, joint position sense, somatosensation, balance, and reflexive joint stability. In Sherrington's13 original description of the “proprioceptive system,” proprioception was used to reference the afferent information arising from “proprioceptors” located in the “proprioceptive field.” The “proprioceptive field” was specifically defined as that area of the body “screened from the environment” by the surface cells, which contained receptors specially adapted for the changes occurring inside the organism independent of the “interoceptive field” (alimentary canal and viscera organs).13 In several of his writings, Sherrington13,14 declared proprioception as being used for the regulation of total posture (postural equilibrium) and segmental posture (joint stability), as well as initiating several conscious peripheral sensations (“muscle senses”). Although he considered vestibular information to be proprioceptive with respect to the head, Sherrington13 clearly delineated the functions of labyrinth from those receptors in the periphery. According to Matthews,15 Sherrington described 4 submodalities of “muscle sense” in Schafer's Textbook of Physiology: (1) posture, (2) passive movement, (3) active movement, and (4) resistance to movement. These submodality sensations correspond to the contemporary terms joint position sense (posture of segment), kinesthesia (active and passive), and the sense of resistance or heaviness. Thus, proprioception correctly describes afferent information arising from internal peripheral areas of the body that contribute to postural control, joint stability, and several conscious sensations.

        In contrast to proprioception, the term somatosensory (or somatosensation) is more global and encompasses all of the mechanoreceptive, thermoreceptive, and pain information arising from the periphery.2 Conscious appreciation of somatosensory information leads to the sensations of pain, temperature, tactile (ie, touch, pressure, etc), and the conscious submodality proprioception sensations. Thus, as Figure 2 illustrates, conscious appreciation of proprioception is a subcomponent of somatosensation and, therefore, the terms should not be used interchangeably.

        Although Sherrington's definition of the proprioceptive field clearly excludes the receptors sensitive to the external environment (“extero-ceptive field”), he did not imply that the receptors in each region function in total exclusion of one another. Rather, Sherrington recognized the interaction between receptors located in both regions of the body, referring to the relationship between the receptors in the exteroceptive and proprioceptive environments as “allied.” Specifically, with respect to conscious proprioception appreciation, this aspect of proprioception has undoubtedly led to much of the confusion surrounding the interpretation of conscious proprioceptive acuity in persons suspected of having diminished proprioceptive information arising from articular sources following orthopaedic injury. Care is required to differentiate between the sources of proprioception and the conscious sensations of proprioception because receptors located in the proprioceptive field may not be the only contributory sources. Depending upon the exact circumstances of a situation or task, sources contributing to conscious sensations of proprioception (ie, joint position sense) could potentially include the deeper receptors (ie, joint and muscle mechanoreceptors) typically associated with proprioception or the more superficial receptors that elicit tactile sensations, or both. Therefore, although the proprioception and tactile sensations are considered to be distinctly different sensory phenomena, similar sensory organs may contribute to each conscious sensation under particular conditions. A complete discussion of the sources contributing to conscious proprioception perception is presented in a later section of this paper.
        
        """
    )

    st.markdown(
        """
        Lastly, mechanoreceptors conveying proprioceptive information are often labeled as proprioceptors.13,14,16,17 However, in addition to mechanoreceptors located in Sherrington's proprioceptive field being referred to as proprioceptors, the term has also been used for the mechanoreceptors located at the surface of the body, and portions of the vestibular apparatus responsible for conveying information regarding the orientation of the head with respect to gravity. Thus, to avoid potential confusion from this wide disparity of use, we recommend utilizing more specific references to the mechanoreceptors of interest.

        Neuromuscular control is a frequently used term in many disciplines related to motor control. It can refer to any of the aspects surrounding nervous system control over muscle activation and the factors contributing to task performance. Specifically, from a joint stability perspective, we define neuromuscular control as the unconscious activation of dynamic restraints occurring in preparation for and in response to joint motion and loading for the purpose of maintaining and restoring functional joint stability. Although neuromuscular control underlies all motor activities in some form, it is not easily separated from the neural commands controlling the overall motor program. For example, in throwing a ball, particular muscle activation sequences occur in the rotator cuff muscles to ensure that the optimal glenohumeral alignment and compression required for joint stability are provided. These muscle activations take place unconsciously and synonymously with the voluntary muscle activations directly associated with the particulars of the task (ie, aiming, speed, distance). Proprioceptive information concerning the status of the joint and associated structures is essential for neuromuscular control. The use of proprioception for motor control and neuromuscular control is the focus of part II of this article.
        """
    )
