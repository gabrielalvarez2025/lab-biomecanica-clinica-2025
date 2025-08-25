import streamlit as st
import numpy as np
import plotly.graph_objects as go

def main_balance():
    st.set_page_config(layout="centered", initial_sidebar_state="expanded")
    st.title("🔺 Simulador interactivo: Teorema del Coseno")

    # Columnas
    col1, col2 = st.columns([1, 2])

    with col1:
        st.markdown("##### Ajusta los lados del triángulo")
        st.markdown(" ")
        st.markdown(" ")

        a = st.slider("Lado A", 1.0, 10.0, 5.0)
        b = st.slider("Lado B", 1.0, 10.0, 5.0)
        c = st.slider("Lado C", 1.0, 10.0, 5.0)

    # --- Columna 2: gráfico ---
    with col2:
        if a + b > c and a + c > b and b + c > a:
            # Construcción del triángulo
            A = np.array([0, 0])
            B = np.array([c, 0])
            x = (a**2 - b**2 + c**2) / (2*c)
            y = np.sqrt(max(a**2 - x**2, 0))
            C = np.array([x, y])

            fig = go.Figure()
            # Lados
            fig.add_trace(go.Scatter(
                x=[A[0], B[0], C[0], A[0]],
                y=[A[1], B[1], C[1], A[1]],
                mode='lines+markers',
                line=dict(color="white", width=3),
                marker=dict(size=12, color='green')
            ))

            # Etiquetas de vértices
            fig.add_trace(go.Scatter(
                x=[A[0], B[0], C[0]],
                y=[A[1], B[1], C[1]],
                mode="text",
                text=["A", "B", "C"],
                textposition="top right",
                showlegend=False
            ))

            # Etiquetas de lados en puntos medios
            offset = 0.3  # separación hacia afuera
            # Puntos medios
            mid_ab = (A + B) / 2
            mid_bc = (B + C) / 2
            mid_ca = (C + A) / 2

            # Normalizaciones para "sacar" la etiqueta hacia afuera
            def desplazar(p1, p2, d):
                v = np.array([p2[1] - p1[1], -(p2[0] - p1[0])])  # vector perpendicular
                v = v / np.linalg.norm(v) if np.linalg.norm(v) > 0 else v
                return (p1 + p2) / 2 + d * v

            pos_a = desplazar(B, C, offset)  # lado a
            pos_b = desplazar(A, C, offset)  # lado b
            pos_c = desplazar(A, B, offset)  # lado c

            fig.add_trace(go.Scatter(
                x=[pos_a[0], pos_b[0], pos_c[0]],
                y=[pos_a[1], pos_b[1], pos_c[1]],
                mode="text",
                text=["A", "B", "C"],
                textposition="middle center",
                showlegend=False
            ))

            # Layout fijo
            max_coord = max(a, b, c) * 1.2
            fig.update_layout(
                width=500,
                height=500,
                xaxis=dict(range=[-1, max_coord], zeroline=False, showgrid=False, visible=False),
                yaxis=dict(range=[-1, max_coord], scaleanchor="x", zeroline=False, showgrid=False, visible=False),
                showlegend=False
            )

            st.plotly_chart(fig, use_container_width=False)

    # Verificar desigualdad triangular
    if a + b > c and a + c > b and b + c > a:
        alpha = np.degrees(np.arccos((b**2 + c**2 - a**2) / (2*b*c)))
        beta  = np.degrees(np.arccos((a**2 - b**2 + c**2) / (2*a*c)))
        gamma = np.degrees(np.arccos((a**2 + b**2 - c**2) / (2*a*b)))

        st.markdown(f"""
        📐 Ángulos calculados (solo para verificación):
        - α (opuesto a A): **{alpha:.2f}°**
        - β (opuesto a B): **{beta:.2f}°**
        - γ (opuesto a C): **{gamma:.2f}°**
        """)
