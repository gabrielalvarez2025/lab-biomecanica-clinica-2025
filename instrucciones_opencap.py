import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def main_instrucciones_opencap():
    st.header("Instrucciones para el uso de OpenCap")

    st.markdown(
        """
       En esta sección encontrarás las instrucciones para el uso de OpenCap, una herramienta de análisis del movimiento humano.
       OpenCap es una plataforma que permite capturar datos cinemáticos a partir de videofotogrametría sin necesidad de marcadores.
        """
    )

    st.markdown(
        """
        El objetivo de este espacio es guiarte a través de los pasos necesarios para utilizar OpenCap de manera fácil, rápida y efectiva.
        """
    )

    st.markdown(
        """
        Para instrucciones más detalladas puedes consultar la documentación y tutoriales oficiales de OpenCap [**aquí**](https://www.opencap.ai/best-practices).
        """
    )

    proporcion = [15, 85]  # Proporción de columnas
    
    # imagenes
    img_laptop = open("images/img_laptop.svg", "r").read()
    img_cellphones2 = open("images/img_cellphones2.svg", "r").read()
    img_appstore = open("images/img_appstore_logo.svg", "r").read()
    img_wifi = open("images/img_wifi_icon.svg", "r").read()
    img_board = open("images/img_board.svg", "r").read()
    img_opencap_logo = "images/img_opencap_logo.png"
    
    
    
    st.markdown("---")

    st.subheader("Requisitos para comenzar:")
    st.markdown(" ")
    
    # Esto determina el orden de las filas, modificar acá
    
    col1_cellphone, col2_cellphone  = st.columns(proporcion)
    col1_laptop,    col2_laptop     = st.columns(proporcion)
    col1_opencap,   col2_opencap    = st.columns(proporcion)
    col1_appstore,  col2_appstore   = st.columns(proporcion)
    col1_wifi,      col2_wifi       = st.columns(proporcion)
    col1_tablero,   col2_tablero    = st.columns(proporcion)
    
    # Fila cellphones
    with col1_cellphone:
        st.image(img_cellphones2, use_container_width=True)
        st.markdown(" ")

    with col2_cellphone:
        st.markdown("""- Al menos **2 dispositivos iOS** (iPhone, iPad, etc) con cámara, que usarás para registrar los videos. Estos necesariamente **deben** ser iOS (marca Apple).""")
    
    
    # Fila laptop
    with col1_laptop:
        st.markdown(" ")
        st.image(img_laptop, use_container_width=True)
        st.markdown(" ")
    
    with col2_laptop:
        st.markdown("""- **Un computador**. Puede ser Windows o Mac. Aquí utilizarás la página Web de OpenCap para iniciar y detener las grabaciones, así como para manejar los datos capturados.
                    Eventualmente puedes usar un celular o una tablet para este propósito, pero este debe ser distinto a los dispositivos que usarás como cámaras, ya que las cámaras no las puedes mover.
                    Te recomendamos usar un computador.
                    """)
        st.markdown(" ")
        
    
    # Fila cuenta opencap
    with col1_opencap:
        st.markdown(" ")
        st.image(img_opencap_logo, use_container_width=True)

    with col2_opencap:
        st.markdown("""- Tener creada una **cuenta en OpenCap**. Si aún no tienes una, puedes crearla de forma gratuita en https://www.opencap.ai/ con tu correo electrónico.""")
        st.markdown(" ")

    # Fila descargar app en appstore
    with col1_appstore:
        st.markdown(" ")
        st.image(img_appstore, use_container_width=True)

    with col2_appstore:
        st.markdown("""- Descargar la App de OpenCap  desde la App Store en todos los dispositivos iOS que usarás como cámara.""")
        st.markdown(" ")

    # Fila wifi
    with col1_wifi:
        st.markdown(" ")
        st.image(img_wifi, use_container_width=True)

    with col2_wifi:
        st.markdown("""- El computador y todos los dispositivos iOS deben estar conectados a la **misma red WiFi**. Esto es fundamental para que los dispositivos puedan comunicarse entre sí y con la plataforma de OpenCap.""")
        #st.markdown(" ")

    
    # Fila tablero calibración
    with col1_tablero:
        st.markdown(" ")
        st.image(img_board, use_container_width=True)

    with col2_tablero:
        st.markdown(" ")
        st.markdown("""- Tener impreso el tablero de calibración, que usarás para la calibración de las cámaras. Puedes descargarlo e imprimirlo desde [aquí](https://cdn.prod.website-files.com/62468717bed6b421c89bbf36/6258dd3518244b061c1b02f5_Checkerboard_4x5_35mm.pdf)""")

        #st.markdown(" ")
    
    
    

    st.markdown("---")

    st.subheader("Preparando el espacio de trabajo")
    
    col_espacio1, col_espacio2 = st.columns([60, 40])

    with col_espacio1:
    
        st.markdown("##### Espacio físico:")
        st.markdown(
            """
            Asegúrate de que el espacio donde realizarás las grabaciones esté bien iluminado y libre de obstáculos. 
            Es importante que el área sea lo suficientemente amplia para que puedas moverte con libertad y que las cámaras puedan capturar todo el movimiento sin obstrucciones.
            """
        )

        st.markdown("##### Cámaras:")
        st.markdown(
            """
            Coloca tus cámaras (iPhones, iPads, etc) sobre trípodes o superficies fijas alrededor del área de grabación.
            Todas la cámaras deben estar fijas y apuntando al lugar donde se ubicará la persona.
            Procura:

            - Mantenerlas quietas, sin moverlas. Idealmente en trípodes.
            - Todas deben apuntar a la zona donde se ubicará la persona.
            - Posiciona las cámaras de forma que durante el movimiento todo el cuerpo de la persona aparezca en la grabación, en todas la cámaras. La persona no debe "salirse de cuadro".
            """
        )
    
    with col_espacio2:
        st.video("https://www.youtube.com/watch?v=LPHeq7bxP38&t=47s", start_time="15s", end_time="32s")
        


    
    


    

    