import streamlit as st

def main_balance():

    
    st.title("Simulación rodilla: Fémur y Tibia")

    # Fijamos la cadera
    cadera = np.array([0, 0])

    # Posición inicial de la rodilla y tobillo
    rodilla = np.array([1, -2])
    tobillo = np.array([2, -4])

    # Creamos figura Plotly
    fig = go.Figure()

    # Dibujar cadera - rodilla (fémur)
    fig.add_trace(go.Scatter(x=[cadera[0], rodilla[0]],
                            y=[cadera[1], rodilla[1]],
                            mode="lines+markers",
                            line=dict(width=5, color="blue"),
                            marker=dict(size=12),
                            name="Fémur"))

    # Dibujar rodilla - tobillo (tibia)
    fig.add_trace(go.Scatter(x=[rodilla[0], tobillo[0]],
                            y=[rodilla[1], tobillo[1]],
                            mode="lines+markers",
                            line=dict(width=5, color="green"),
                            marker=dict(size=12),
                            name="Tibia"))

    # Configuración interactiva: se puede arrastrar la rodilla
    fig.update_layout(
        dragmode="drawopenpath", # permite dibujar/arrastrar
        xaxis=dict(scaleanchor="y", range=[-5, 5]),
        yaxis=dict(range=[-6, 2]),
        showlegend=False,
        height=600
    )

    st.plotly_chart(fig, use_container_width=True)

    st.markdown("👉 Arrastra la rodilla y observa cómo cambia el ángulo (en versión interactiva se puede calcular si guardamos el nuevo punto).")

    # Ejemplo de cálculo del ángulo (cuando tengamos la rodilla movida)
    def calcular_angulo(cadera, rodilla, tobillo):
        v1 = cadera - rodilla
        v2 = tobillo - rodilla
        cos_theta = np.dot(v1, v2) / (np.linalg.norm(v1) * np.linalg.norm(v2))
        angulo = np.degrees(np.arccos(np.clip(cos_theta, -1.0, 1.0)))
        return angulo

    angulo = calcular_angulo(cadera, rodilla, tobillo)
    st.write(f"Ángulo actual rodilla: {angulo:.2f}°")

    

    