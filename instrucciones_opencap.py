import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def instrucciones():
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

    st.markdown("---")

    st.subheader("Antes de comenzar: Preparación")

    st.markdown(
        """
        Para utilizar OpenCap, primero debes:

        
        - Contar con **dos o más** dispositivos iOS (iPhone, iPad, etc) con cámara. Estos deben ser iOS (marca Apple).
        - Descargar la aplicación de OpenCap en ambos dispositivos iOS desde la App Store.
        - Disponer de un espacio bien iluminado y más bien amplio para realizar las grabaciones.
        """
    )

    proporcion = [15, 85]  # Proporción de columnas
    
    # imagenes
    img_laptop = open("img_laptop.svg", "r").read()
    img_cellphones2 = open("img_cellphones2.svg", "r").read()
    
    
    
    st.markdown("---")

    st.subheader("Requisitos para comenzar:")
    st.markdown(" ")
    
    # Esto determina el orden de las filas, modificar acá
    col1_opencap,    col2_opencap   = st.columns(proporcion)
    col1_cellphone, col2_cellphone  = st.columns(proporcion)
    col1_laptop,    col2_laptop     = st.columns(proporcion)
    
    
    
    # Fila cuenta opencap
    with col1_opencap:
        st.image("img_opencap_logo.png", use_container_width=True)

    with col2_opencap:
        st.markdown("""- Debes **crear una cuenta en OpenCap**. Puedes crear una cuenta gratuita en https://www.opencap.ai/ con tu correo electrónico.""")
        st.markdown(" ")
    


    # Fila cellphones
    with col1_cellphone:
        st.image(img_cellphones2, use_container_width=True)
        st.markdown(" ")
        st.markdown(" ")

    with col2_cellphone:
        st.markdown("""- Al menos 2 dispositivos iOS (iPhone, iPad, etc) con cámara, que usarás para registrar los videos. Estos necesariamente **deben** ser iOS (marca Apple).""")
    
    
    # Fila laptop
    with col1_laptop:
        st.markdown(" ")
        st.image(img_laptop, use_container_width=True)
        st.markdown(" ")
    
    with col2_laptop:
        st.markdown("""- Un computador. Puede ser Windows o Mac. Aquí utilizarás la página Web de OpenCap para iniciar y detener las grabaciones, así como para manejar los datos capturados.
                    Eventualmente puedes usar un celular o una tablet para este propósito, pero este debe ser distinto a los dispositivos que usarás como cámaras, ya que las cámaras no las puedes mover.
                    """)


    st.markdown("---")

    
    


    

    