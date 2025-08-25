import streamlit as st
import numpy as np
import plotly.graph_objects as go
import random

def generar_triangulo():
    """Genera lados válidos de un triángulo usando desigualdad triangular"""
    while True:
        a = random.uniform(2, 10)  # BC
        b = random.uniform(2, 10)  # AC
        c = random.uniform(2, 10)  # AB
        if a + b > c and a + c > b and b + c > a:
            return a, b, c

def main_balance():
    st.set_page_config(layout="centered", initial_sidebar_state="expanded")
    st.title("🔺 Simulador interactivo: Teorema del Coseno")

    # Estado de los lados
    if "lados" not in st.session_state:
        st.session_state.lados = generar_triangulo()

    # Botón para generar nuevos lados
    if st.button("🎲 Generar triángulo aleatorio"):
        st.session_state.lados = generar_triangulo()

    a, b, c = st.session_state.lados  # lados: a=BC, b=AC, c=AB

    # --- Construcción del triángulo ---
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

    # Función para desplazar etiquetas de lados hacia afuera
    def desplazar(p1, p2, d):
        v = np.array([p2[1] - p1[1], -(p2[0] - p1[0])])  # vector perpendicular
        v = v / np.linalg.norm(v) if np.linalg.norm(v) > 0 else v
        return (p1 + p2) / 2 + d * v

    offset = 0.3
    pos_ab = desplazar(A, B, offset)  # lado c = AB
    pos_bc = desplazar(B, C, offset)  # lado a = BC
    pos_ac = desplazar(A, C, offset)  # lado b = AC

    # Etiquetas de lados
    fig.add_trace(go.Scatter(
        x=[pos_ab[0], pos_bc[0], pos_ac[0]],
        y=[pos_ab[1], pos_bc[1], pos_ac[1]],
        mode="text",
        text=["c", "a", "b"],  # nomenclatura correcta
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

    # --- Cálculo de ángulos ---
    alpha = np.degrees(np.arccos((b**2 + c**2 - a**2) / (2*b*c)))
    beta  = np.degrees(np.arccos((a**2 + c**2 - b**2) / (2*a*c)))
    gamma = np.degrees(np.arccos((a**2 + b**2 - c**2) / (2*a*b)))

    # Columnas para gráfico y datos
    col1, col2 = st.columns(2)

    with col1:
        st.markdown("## Datos del triángulo:")
        st.markdown(f"""
        - **Lados**  
            • a = {a:.2f}  
            • b = {b:.2f}  
            • c = {c:.2f}  
        """)
        st.markdown(f"""
        - **Ángulos**  
            • α (en A) = {alpha:.2f}°  
            • β (en B) = {beta:.2f}°  
            • γ (en C) = {gamma:.2f}°  
        """)

    with col2:
        st.plotly_chart(fig, use_container_width=False)

    # Fórmula del coseno centrada con colores pasteles
    st.markdown(r"""
    <div style="text-align:center; font-size:30px; line-height:1.5;">
    c<sup>2</sup> = 
    <span style="color:#FFB3BA;">a</span><sup>2</sup> + 
    <span style="color:#BAE1FF;">b</span><sup>2</sup> - 
    2<span style="color:#FFDFBA;">a</span><span style="color:#BAE1FF;">b</span> · cos(<span style="color:#BAFFC9;">γ</span>)
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")
