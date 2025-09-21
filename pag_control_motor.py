import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import plotly.express as px
import pandas as pd
from pydub import AudioSegment

def main_control_motor():
    st.markdown("#### Teorías del control motor")



    

    # Ejemplo de eventos
    data = {
        "Tarea": ["Preparar experimento", "Recolectar datos", "Analizar resultados", "Escribir informe"],
        "Inicio": ["2025-09-01", "2025-09-05", "2025-09-12", "2025-09-20"],
        "Fin":    ["2025-09-04", "2025-09-10", "2025-09-18", "2025-09-25"]
    }

    df = pd.DataFrame(data)

    # Crear timeline
    fig = px.timeline(df, x_start="Inicio", x_end="Fin", y="Tarea", color="Tarea")
    fig.update_yaxes(autorange="reversed")  # Para que quede estilo cronológico

    st.plotly_chart(fig, use_container_width=True)