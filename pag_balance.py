import streamlit as st
import numpy as np
import plotly.graph_objects as go


def main_balance():

    # Configuración fija de la página
    st.set_page_config(
        layout="centered",          # mantener layout ancho
        initial_sidebar_state="expanded"
    )

    st.title("🔺 Simulador interactivo: Teorema del Coseno")

    # Crear columnas: col1 sliders, col2 gráfico
    col1, col2 = st.columns([1, 2])

    # --- Columna 1: sliders y ángulos ---
    with col1:
        st.subheader("Ajusta los lados del triángulo")
        a = st.slider("Lado a", 1.0, 10.0, 5.0)
        b = st.slider("Lado b", 1.0, 10.0, 5.0)
        c = st.slider("Lado c", 1.0, 10.0, 5.0)

        # Verificar desigualdad triangular
        if a + b > c and a + c > b and b + c > a:
            # Calcular ángulos con teorema del coseno
            alpha = np.degrees(np.arccos((b**2 + c**2 - a**2) / (2*b*c)))
            beta  = np.degrees(np.arccos((a**2 + c**2 - b**2) / (2*a*c)))
            gamma = np.degrees(np.arccos((a**2 + b**2 - c**2) / (2*a*b)))

            st.markdown(f"""
            📐 Ángulos calculados:
            - α (opuesto a a): **{alpha:.2f}°**
            - β (opuesto a b): **{beta:.2f}°**
            - γ (opuesto a c): **{gamma:.2f}°**
            """)
        else:
            st.error("❌ Los lados no cumplen la desigualdad triangular.")

    # --- Columna 2: gráfico fijo ---
    with col2:
        st.subheader("Triángulo")

        if a + b > c and a + c > b and b + c > a:
            # Coordenadas del triángulo
            A = np.array([0, 0])
            B = np.array([c, 0])
            x = (a**2 - b**2 + c**2) / (2*c)
            y = np.sqrt(max(a**2 - x**2, 0))
            C = np.array([x, y])

            # Crear gráfico Plotly con tamaño fijo
            fig = go.Figure()

            # Líneas y puntos del triángulo
            fig.add_trace(go.Scatter(
                x=[A[0], B[0], C[0], A[0]],
                y=[A[1], B[1], C[1], A[1]],
                mode='lines+markers+text',
                text=["A", "B", "C", ""],
                textposition="top right",
                line=dict(color="blue", width=3),
                marker=dict(size=8, color='black')
            ))

            # Mantener la misma escala y tamaño fijo
            max_coord = max(a, b, c) * 1.2
            fig.update_layout(
                width=500,
                height=500,
                xaxis=dict(range=[-1, max_coord], zeroline=False, showgrid=False, visible=False),
                yaxis=dict(range=[-1, max_coord], scaleanchor="x", zeroline=False, showgrid=False, visible=False),
                showlegend=False
            )

            # Mostrar gráfico sin que el contenedor cambie de tamaño
            st.plotly_chart(fig, use_container_width=False)