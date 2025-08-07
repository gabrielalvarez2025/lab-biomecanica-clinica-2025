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
        Para utilizar OpenCap, asegúrate de tener lo siguiente:
        - Crear una cuenta en OpenCap. Puedes crear una cuenta gratuita en https://www.opencap.ai/ con tu correo electrónico.
        - Contar con **dos o más** dispositivos iOS (iPhone, iPad, etc) con cámara. Estos deben ser iOS (marca Apple).
        - Descargar la aplicación de OpenCap en ambos dispositivos iOS desde la App Store.
        - Disponer de un espacio bien iluminado y más bien amplio para realizar las grabaciones.
        """
    )

    st.markdown(
        """
        - 📱📱 Al menos 2 dispositivos iOS (iPhone, iPad, etc) con cámara, que usarás para registrar los videos. Estos necesariamente **deben** ser iOS (marca Apple).
        
        - ‍💻 Un computador. Eventualmente puede ser un celular o una tablet, pero debe ser distinto a los dispositivos que usarás como cámaras.
        
        - Disponer de un espacio bien iluminado y más bien amplio para realizar las grabaciones.
        """
    )

    st.markdown(
        """
        Luego, debes asegurart de que:
        - Los +2 dispositivos iOS estén conectados a la misma red Wi-Fi.
        """
    )