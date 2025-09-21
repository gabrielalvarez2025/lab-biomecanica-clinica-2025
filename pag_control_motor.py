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
            "T. refleja",
            "T. jerárquica",
            "T. de los Programas Motores",
            "T. de Modelos internos",
            "Hip. del Manifold No-controlado (UCM)",
            "Sistemas dinámicos"
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
        text="Teoría",   # Etiquetas sobre las barras
        title="Cronología de teorías del control motor",
    )

    fig.update_traces(
        textposition="inside",  # texto dentro de las barras
        insidetextanchor="middle",  # centrado
        textfont=dict(
            color="k",     # color blanco
            size=9            # mismo tamaño para todas
        )
    )
    fig.update_yaxes(autorange="reversed", showticklabels=False)

    # Ajustes de layout
    fig.update_layout(
        xaxis_title="Año",
        yaxis_title="",
        hovermode="closest",
        height=600,
        legend=dict(
            orientation="h",
            y=-0.2,
            x=0.5,
            xanchor="center"
        )
    )

    # Grid vertical cada 5 años
    fig.update_xaxes(
        tickformat="%Y",
        dtick="M120",         # cada 60 meses = 5 años
        showgrid=True,
        gridcolor="lightgray"
    )

    st.plotly_chart(fig, use_container_width=True)


    tabs = st.tabs([
        "Teoría refleja",
        "Teoría jerárquica",
        "Teoría de los programas motores",
        "Modelos internos",
        "Hipótesis UCM",
        "Sistemas dinámicos"
    ])

    with tabs[0]:
        st.markdown("### 🔹 Teoría refleja (1900–1930)")
        st.markdown(
            """
            - Basada en **arcos reflejos** como unidad fundamental del movimiento.  
            - El movimiento se explica como la suma de reflejos simples.  
            - Limitación: no puede explicar movimientos voluntarios complejos.  
            """
        )

    with tabs[1]:
        st.markdown("### 🔹 Teoría jerárquica (1930–1960)")
        st.markdown(
            """
            - El control motor se organiza en **niveles jerárquicos** (corteza, tronco encefálico, médula).  
            - El nivel superior domina a los inferiores.  
            - Limitación: hoy sabemos que los niveles inferiores también influyen en los superiores.  
            """
        )

    with tabs[2]:
        st.markdown("### 🔹 Teoría de los programas motores (1960–1980)")
        st.markdown(
            """
            - Propone la existencia de **programas motores almacenados** que generan patrones de movimiento.  
            - Ejemplo: esquema de movimientos como "caminar" o "escribir".  
            - Limitación: no explica la flexibilidad y adaptación en entornos cambiantes.  
            """
        )

    with tabs[3]:
        st.markdown("### 🔹 Modelos internos (1980–actualidad)")
        st.markdown(
            """
            - Basados en **neurociencias computacionales**.  
            - El cerebro construye modelos para predecir (modelo directo) y calcular comandos (modelo inverso).  
            - Útiles para explicar aprendizaje motor y control predictivo.  
            """
        )

    with tabs[4]:
        st.markdown("### 🔹 Hipótesis del Manifold No Controlado (UCM) (1990–actualidad)")
        st.markdown(
            """
            - Propuesta por **Latash y colaboradores**.  
            - El sistema motor **no controla cada grado de libertad**, sino que organiza variabilidad hacia tareas relevantes.  
            - Explica la **coordinación y redundancia** en el movimiento.  
            """
        )

    with tabs[5]:
        st.markdown("### 🔹 Teoría de los sistemas dinámicos (2000–actualidad)")
        st.markdown(
            """
            - Inspirada en la teoría de sistemas complejos.  
            - El movimiento surge de la **autoorganización** entre individuo, tarea y entorno.  
            - Explica fenómenos como transiciones súbitas en patrones de movimiento.  
            """
        )