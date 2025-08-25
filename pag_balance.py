import streamlit as st
import numpy as np
import plotly.graph_objects as go

def calcular_ortocentro(A, B, C):
    """
    Calcula el ortocentro de un triángulo con vértices A, B, C
    usando intersección de alturas (puro numpy).
    """
    x1, y1 = A
    x2, y2 = B
    x3, y3 = C

    # Pendientes de los lados
    mAB = (y2 - y1) / (x2 - x1) if x2 != x1 else None
    mBC = (y3 - y2) / (x3 - x2) if x3 != x2 else None
    mCA = (y1 - y3) / (x1 - x3) if x1 != x3 else None

    # Altura desde A (perpendicular a BC)
    if mBC is None:  # BC vertical → altura horizontal
        xh1 = x1
        yh1 = y2
    elif mBC == 0:   # BC horizontal → altura vertical
        xh1 = x1
        yh1 = y1
    else:
        m_alturaA = -1 / mBC
        # y - y1 = m*(x - x1)
        # Recta altura_A: pasa por A con pendiente m_alturaA
        # La segunda la hallamos luego

    # Altura desde B (perpendicular a AC)
    if mCA is None:  # AC vertical → altura horizontal
        xh2 = x2
        yh2 = y1
    elif mCA == 0:   # AC horizontal → altura vertical
        xh2 = x2
        yh2 = y2
    else:
        m_alturaB = -1 / mCA

    # Resolver intersección de dos rectas (altura_A y altura_B)
    if (mBC not in [None, 0]) and (mCA not in [None, 0]):
        # Ecuación altura A: y = m_alturaA*(x - x1) + y1
        # Ecuación altura B: y = m_alturaB*(x - x2) + y2
        A1 = m_alturaA
        B1 = -1
        C1 = y1 - m_alturaA * x1

        A2 = m_alturaB
        B2 = -1
        C2 = y2 - m_alturaB * x2

        det = A1 * B2 - A2 * B1
        if det == 0:  # Colineal o degenerado
            return (np.nan, np.nan)
        Hx = (B1 * C2 - B2 * C1) / det
        Hy = (C1 * A2 - C2 * A1) / det
    else:
        # Casos degenerados (rectas verticales/horizontales)
        if mBC is None:   # altura desde A es vertical
            Hx = x1
            Hy = m_alturaB * (x1 - x2) + y2
        elif mBC == 0:    # altura desde A es horizontal
            Hy = y1
            Hx = (Hy - y2) / m_alturaB + x2
        elif mCA is None: # altura desde B es vertical
            Hx = x2
            Hy = m_alturaA * (x2 - x1) + y1
        elif mCA == 0:    # altura desde B es horizontal
            Hy = y2
            Hx = (Hy - y1) / m_alturaA + x1
        else:
            Hx, Hy = np.nan, np.nan

    return float(Hx), float(Hy)


def main_balance():
    st.set_page_config(layout="centered", initial_sidebar_state="expanded")
    st.title("🔺 Simulador interactivo: Teorema del Coseno")

    # Columnas
    col1, col2 = st.columns([1, 2], gap="large")

    with col1:
        st.markdown("##### Ajusta los lados del triángulo")
        st.markdown(" ")

        a = st.slider("Lado A", 1.0, 10.0, 5.0)
        b = st.slider("Lado B", 1.0, 10.0, 5.0)
        c = st.slider("Lado C", 1.0, 10.0, 5.0)

    # --- Columna 2: gráfico ---
    with col2:
        st.subheader("Triángulo")

        with st.container():
            if a + b > c and a + c > b and b + c > a:
                # Construcción del triángulo
                A = np.array([0, 0])
                B = np.array([c, 0])
                x = (a**2 - b**2 + c**2) / (2*c)
                y = np.sqrt(max(a**2 - x**2, 0))
                C = np.array([x, y])

                # Ortocentro con numpy
                Hx, Hy = calcular_ortocentro(A, B, C)

                # Distancias máximas desde ortocentro a vértices
                dx = max(abs(Hx - A[0]), abs(Hx - B[0]), abs(Hx - C[0]))
                dy = max(abs(Hy - A[1]), abs(Hy - B[1]), abs(Hy - C[1]))
                rango = max(dx, dy) * 1.2

                # Gráfico
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=[A[0], B[0], C[0], A[0]],
                    y=[A[1], B[1], C[1], A[1]],
                    mode='lines+markers+text',
                    text=["A", "B", "C", ""],
                    textposition="top right",
                    line=dict(color="white", width=3),
                    marker=dict(size=15, color='green')
                ))

                # Ortocentro
                fig.add_trace(go.Scatter(
                    x=[Hx], y=[Hy],
                    mode="markers+text",
                    text=["H"],
                    textposition="bottom center",
                    marker=dict(size=12, color="red", symbol="x"),
                    name="Ortocentro"
                ))

                # Centrar ortocentro
                fig.update_layout(
                    width=500,
                    height=500,
                    autosize=False,
                    xaxis=dict(range=[Hx - rango, Hx + rango],
                               scaleanchor="y", zeroline=False, showgrid=False, visible=False),
                    yaxis=dict(range=[Hy - rango, Hy + rango],
                               zeroline=False, showgrid=False, visible=False),
                    showlegend=False,
                    margin=dict(l=20, r=20, t=20, b=20)
                )

                st.plotly_chart(fig, use_container_width=False)
            else:
                st.error("❌ Los lados no cumplen la desigualdad triangular.")
