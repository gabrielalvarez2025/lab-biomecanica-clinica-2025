import streamlit as st
import numpy as np
from math import acos, degrees
from streamlit_drawable_canvas import st_canvas

def main_balance():

    
    st.set_page_config(layout="wide")
    st.title("Simulación rodilla: Fémur y Tibia")

    # Parámetros iniciales
    cadera = np.array([200, 100])   # fija
    rodilla = np.array([200, 250])  # arrastrable
    tobillo = np.array([200, 400])  # fijo (solo para demo)

    # --- Dibujo con Canvas ---
    st.subheader("Mueve la rodilla (punto rojo) con el mouse")

    canvas_result = st_canvas(
        fill_color="rgba(255, 0, 0, 0.3)",  # color del punto
        stroke_width=3,
        stroke_color="red",
        background_color="white",
        update_streamlit=True,
        height=500,
        width=500,
        drawing_mode="transform",   # permite mover shapes
        initial_drawing={
            "version": "4.4.0",
            "objects": [
                {"type": "circle", "left": rodilla[0], "top": rodilla[1], "radius": 8,
                "fill": "red", "stroke": "black"},
            ],
        },
        key="canvas",
    )

    # --- Cálculo del ángulo ---
    def calcular_angulo(cadera, rodilla, tobillo):
        v1 = cadera - rodilla
        v2 = tobillo - rodilla
        cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angulo = degrees(acos(np.clip(cos_theta, -1.0, 1.0)))
        return angulo

    if canvas_result.json_data is not None:
        objetos = canvas_result.json_data["objects"]
        if objetos:
            # obtener nueva posición de la rodilla
            rodilla_x = objetos[0]["left"]
            rodilla_y = objetos[0]["top"]
            rodilla = np.array([rodilla_x, rodilla_y])

            # calcular ángulo
            angulo = calcular_angulo(cadera, rodilla, tobillo)

            st.write(f"📐 Ángulo de la rodilla: **{angulo:.2f}°**")

            # mostramos dibujo de segmentos
            import matplotlib.pyplot as plt
            fig, ax = plt.subplots()
            ax.plot([cadera[0], rodilla[0]], [cadera[1], rodilla[1]], "b-o", label="Fémur")
            ax.plot([rodilla[0], tobillo[0]], [rodilla[1], tobillo[1]], "g-o", label="Tibia")
            ax.plot(cadera[0], cadera[1], "ko", markersize=10, label="Cadera fija")
            ax.set_xlim(100, 300)
            ax.set_ylim(50, 450)
            ax.invert_yaxis()  # para que coincida con coordenadas canvas
            ax.legend()
            st.pyplot(fig)
    

    