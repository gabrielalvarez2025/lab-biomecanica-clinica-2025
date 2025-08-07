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

        - Crear una cuenta en OpenCap. Puedes crear una cuenta gratuita en https://www.opencap.ai/ con tu correo electrónico.
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
    
    st.subheader("Dispositivos necesarios:")
    st.markdown(" ")
    
    # Esto determina el orden de las filas, modificar acá
    col1_cellphone, col2_cellphone  = st.columns(proporcion)
    col1_laptop,    col2_laptop     = st.columns(proporcion)
    
    
    # Fila cellphones
    with col1_cellphone:
        st.image(img_cellphones2, use_container_width=True)
        st.markdown(" ")
        st.markdown(" ")

    with col2_cellphone:
        st.markdown("""- Al menos 2 dispositivos iOS (iPhone, iPad, etc) con cámara, que usarás para registrar los videos. Estos necesariamente **deben** ser iOS (marca Apple).""")
    
    
    # Fila laptop
    with col1_laptop:
        st.image(img_laptop, use_container_width=True)
        st.markdown(" ")
        st.markdown(" ")
    
    with col2_laptop:
        st.markdown("""- Un computador. Eventualmente puede ser un celular o una tablet, pero debe ser distinto a los dispositivos que usarás como cámaras.""")


    st.markdown("---")

    
    


    

    