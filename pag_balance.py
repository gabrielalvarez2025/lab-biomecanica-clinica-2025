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
        a = st.slider("Lado A", 1.0, 10.0, 5.0)
        b = st.slider("Lado B", 1.0, 10.0, 5.0)
        c = st.slider("Lado C", 1.0, 10.0, 5.0)

        

    # --- Columna 2: gráfico ---
    with col2:
        
        if a + b > c and a + c > b and b + c > a:
            A = np.array([0,0])
            B = np.array([c,0])
            x = (a**2 - b**2 + c**2) / (2*c)
            y = np.sqrt(max(a**2 - x**2, 0))
            C = np.array([x,y])

            fig = go.Figure()
            fig.add_trace(go.Scatter(
                x=[A[0], B[0], C[0], A[0]],
                y=[A[1], B[1], C[1], A[1]],
                mode='lines+markers+text',
                text=["A","B","C",""],
                textposition="top right",
                line=dict(color="white", width=3),
                marker=dict(size=8, color='red')
            ))
            max_coord = max(a,b,c)*1.2
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
        beta  = np.degrees(np.arccos((a**2 + c**2 - b**2) / (2*a*c)))
        gamma = np.degrees(np.arccos((a**2 + b**2 - c**2) / (2*a*b)))

        st.markdown(f"""
        📐 Ángulos calculados (solo para verificación):
        - α (opuesto a A): **{alpha:.2f}°**
        - β (opuesto a B): **{beta:.2f}°**
        - γ (opuesto a C): **{gamma:.2f}°**
        """)

        st.subheader("Prueba tus conocimientos")
        dato_faltante = st.selectbox(
            "¿Qué dato quieres calcular?",
            ["Ángulo α", "Ángulo β", "Ángulo γ", "Lado A", "Lado B", "Lado C"]
        )
        respuesta = st.number_input("Ingresa tu respuesta", min_value=0.0, step=0.01)

        if st.button("Verificar"):
            correcto = None
            if dato_faltante == "Ángulo α":
                correcto = alpha
            elif dato_faltante == "Ángulo β":
                correcto = beta
            elif dato_faltante == "Ángulo γ":
                correcto = gamma
            elif dato_faltante == "Lado a":
                correcto = a
            elif dato_faltante == "Lado b":
                correcto = b
            elif dato_faltante == "Lado c":
                correcto = c

            if abs(respuesta - correcto) < 0.5:  # tolerancia de 0.5
                st.success(f"✅ Correcto! El valor es aproximadamente {correcto:.2f}")
            else:
                st.error(f"❌ Incorrecto. El valor correcto es {correcto:.2f}")

    else:
        st.error("❌ No es posible dibujar un triángulo con esta combinación de lados. Los lados no cumplen la desigualdad triangular.")
