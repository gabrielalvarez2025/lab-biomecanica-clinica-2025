import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from pydub import AudioSegment

def main_control_motor():
    st.markdown("#### Teorías del control motor")



    

    # Datos de la cronología (más realista)
    data = {
        "Teoría": [
            "Teoría refleja",
            "Teoría jerárquica",
            "Teoría de los programas motores",
            "Modelos internos (directo e inverso)",
            "Hipótesis del Manifold No-controlado (UCM)",
            "Teoría de los sistemas dinámicos"
        ],
        "Inicio": [
            "1900-01-01",   # Refleja (Sherrington, principios del siglo XX)
            "1930-01-01",   # Jerárquica (Jackson, Magnus)
            "1960-01-01",   # Programas motores (Keele, Schmidt, 60s-70s)
            "1980-01-01",   # Modelos internos (Kawato, Wolpert, 80s-90s)
            "1990-01-01",   # UCM (Scholz & Schöner, 90s)
            "1990-01-01"    # Sistemas dinámicos (Kelso, 80s-90s, pero vigentes)
        ],
        "Fin": [
            "1950-01-01",   # Refleja → superada por otras
            "1970-01-01",   # Jerárquica → crítica con evidencia posterior
            "1990-01-01",   # Programas motores → cuestionados
            "2025-01-01",   # Modelos internos → aún vigentes
            "2025-01-01",   # UCM → actual
            "2025-01-01"    # Sistemas dinámicos → actual
        ]
    }

    # Crear DataFrame
    df = pd.DataFrame(data)
    df["Inicio"] = pd.to_datetime(df["Inicio"])
    df["Fin"] = pd.to_datetime(df["Fin"])

    # Timeline con Plotly
    fig = px.timeline(
        df,
        x_start="Inicio",
        x_end="Fin",
        y="Teoría",
        color="Teoría",
        text="Teoría",   # Agregar etiquetas
        title="Cronología de teorías del control motor",
    )

    fig.update_traces(textposition="outside")  # Poner etiquetas sobre la barra
    fig.update_yaxes(autorange="reversed")     # Para que empiece desde arriba

    # Ajustes de layout
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="",
        hovermode="closest",
        height=600,
        legend=dict(
            orientation="h",    # Horizontal
            y=-0.2,             # Debajo del gráfico
            x=0.5,              # Centrado
            xanchor="center"
        )
    )

    st.plotly_chart(fig, use_container_width=True)