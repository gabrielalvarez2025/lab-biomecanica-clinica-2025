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

    st. markdown("OpenCap es bastante flexible y generalmente no tiene problemas para capturar buenos datos en la mayoría de los casos. Te dejamos algunos requisitos infaltables y algunas recomendaciones de buenas prácticas para que te asegures de que OpenCap no tenga conflictos al momento de tomar los datos")
    
    col_espacio1, col_espacio2 = st.columns([40, 60])

    with col_espacio1:
        st.success(
            """
            ##### Espacio físico:

            Asegúrate de que el espacio donde realizarás las grabaciones esté **bien iluminado** 💡 y libre de obstáculos. 
            
            Es importante que el área sea lo suficientemente amplia para que la persona pueda moverse con libertad y que las cámaras puedan capturar todo el movimiento sin obstrucciones.
            """
        )
        st.warning(
            """
            ##### Persona:

            - Prefiere ropa ajustada 👖 por sobre holgada

            - Prefiere ropa de un color que contraste ◑ con el fondo.

            - Prefiere zapatillas que contrasten con el suelo y con el pantalón.
            """
        )

        

    with col_espacio2:
        st.info(
            """
            ##### Cámaras:
            
            Coloca tus cámaras (iPhones, iPads, etc) alrededor del área de grabación. Usaremos la cámara trasera de tus dispositivos.
            
            **Todas la cámaras deben:**
             
            - Estar fijas, estáticas, idealmente en trípodes.

            - Orientarse para grabación vertical.

            - Apuntar a la zona donde se ubicará la persona.
            
            - Estar posicionadas de forma que durante el movimiento todo el cuerpo de la persona aparezca en la grabación. La persona no debe "salirse de cuadro".
        
            - Evita que otras personas se crucen o aparezcan en el video.

            - Evita que la persona entre/salga de la zona de grabación.
            """
        )
    

    st.markdown(
        """
        
       

        """
    )
        


    
    


    

    