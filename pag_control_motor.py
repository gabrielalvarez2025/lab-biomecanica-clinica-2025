import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from pydub import AudioSegment

def main_control_motor():
    st.markdown("#### Teorías del control motor")



    

    st.markdown("### 📜 Línea de tiempo de las teorías del control motor")

    # Datos de teorías (fechas aproximadas para ilustrar)
    data = {
        "Teoría": [
            "Teoría refleja",
            "Teoría jerárquica",
            "Teoría de los programas motores",
            "Modelos internos (directo e inverso)",
            "Hipótesis del Manifold Incontrolado (UCM)",
            "Teoría de los sistemas dinámicos"
        ],
        "Inicio": [
            "1900-01-01",   # Refleja
            "1930-01-01",   # Jerárquica
            "1960-01-01",   # Programas motores
            "1980-01-01",   # Modelos internos
            "1990-01-01",   # UCM
            "2000-01-01"    # Sistemas dinámicos
        ],
        "Fin": [
            "1930-01-01",   # Fin reflejo
            "1960-01-01",   # Fin jerárquica
            "1980-01-01",   # Fin programas motores
            "1990-01-01",   # Fin modelos internos
            "2000-01-01",   # Fin UCM
            "2025-01-01"    # Actualidad
        ]
    }

    df = pd.DataFrame(data)

    # Crear timeline
    fig = px.timeline(df, x_start="Inicio", x_end="Fin", y="Teoría", color="Teoría")
    fig.update_yaxes(autorange="reversed")  # orden cronológico de arriba hacia abajo
    fig.update_layout(
        height=500,
        title="Evolución de las teorías del control motor",
        xaxis_title="Año",
        yaxis_title="Teoría",
        legend=dict(orientation="h", y=-0.2)
    )

    st.plotly_chart(fig, use_container_width=True)