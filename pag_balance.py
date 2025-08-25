import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

def main_balance():

    st.set_page_config(layout="wide")
    st.title("Simulador interactivo: Teorema del Coseno")

    st.markdown("""
    El **Teorema del Coseno** dice que en un triángulo con lados `a`, `b`, `c` y ángulo opuesto a `c` (γ):

    \[
    c^2 = a^2 + b^2 - 2ab \cdot \cos(\gamma)
    \]
    """)

    # Sliders para los lados
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

        # Dibujar triángulo
        # Colocamos el triángulo en coordenadas 2D
        A = np.array([0, 0])
        B = np.array([c, 0])  # lado c en la base
        # Usar ley de cosenos para encontrar coordenada de C
        x = (a**2 - b**2 + c**2) / (2*c)
        y = np.sqrt(max(a**2 - x**2, 0))
        C = np.array([x, y])

        fig, ax = plt.subplots()
        ax.plot([A[0], B[0]], [A[1], B[1]], "b-", lw=2, label="c")
        ax.plot([B[0], C[0]], [B[1], C[1]], "g-", lw=2, label="a")
        ax.plot([C[0], A[0]], [C[1], A[1]], "r-", lw=2, label="b")

        # Puntos
        ax.plot(*A, "ko")
        ax.text(A[0], A[1]-0.2, "A")
        ax.plot(*B, "ko")
        ax.text(B[0], B[1]-0.2, "B")
        ax.plot(*C, "ko")
        ax.text(C[0], C[1]+0.2, "C")

        ax.set_aspect("equal")
        ax.legend()
        st.pyplot(fig)

    else:
        st.error("❌ Los lados no cumplen la desigualdad triangular. No existe un triángulo con esas medidas.")
