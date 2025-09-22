import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import plotly.express as px
import plotly.graph_objects as go
from scipy.stats import chi2
from pydub import AudioSegment

def main_control_motor():
    st.markdown("#### Teorías del control motor")


    data = {
        "Teoría": [
            "T. Refleja",
            "T. Jerárquica",
            "Ts. de Programación Motora",
            "T. de Sistemas",
            "T. de Sistemas Dinámicos",
            "T. Ecológica",
            "T. Modelos Internos",
            "Hip. Manifold No-Controlado (UCM)"
        ],
        "Inicio": [
            "1906-01-01",  # Refleja (Sherrington, principios del siglo XX)
            "1930-01-01",  # Jerárquica (Jackson, Magnus)
            "1960-01-01",  # Programas Motores (Bernstein, Keele, 1960s)
            "1920-01-01",  # Sistemas (Bernstein, desarrollo inicial)
            "1980-01-01",  # Sistemas Dinámicos (Kelso, 1980s)
            "1960-01-01",  # Ecológica (Gibson, 1960s)
            "1980-01-01",  # Modelos Internos (Kawato, Wolpert, 80s-90s)
            "1990-01-01"   # UCM (Scholz & Schöner, 1990s)
        ],
        "Fin": [
            "1950-01-01",  # Refleja
            "1970-01-01",  # Jerárquica
            "1990-01-01",  # Programas Motores
            "1966-01-01",  # Sistemas (Bernstein fallece, evolución a dinámicos)
            "2025-01-01",  # Sistemas Dinámicos → vigente
            "2025-01-01",  # Ecológica → vigente
            "2025-01-01",  # Modelos Internos → vigente
            "2025-01-01"   # UCM → vigente
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
            color="black",     # color blanco
            size=12            # mismo tamaño para todas
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


    

    

    st.markdown("## Teorías del Control Motor")

    # Crear tabs para cada teoría
    tab_intro, tab_refleja, tab_jerarquica, tab_pm, tab_sistemas, tab_dinamicos, tab_ecologica = st.tabs([
        "🔎",
        "Teoría Refleja",
        "Teoría Jerárquica",
        "Programación Motora",
        "Teoría de Sistemas",
        "Sistemas Dinámicos",
        "Teoría Ecológica"
    ])

    
    with tab_intro:
        st.markdown("Explora esta sección para conocer las principales teorías del control motor (pasadas y actuales), sus postulados, limitaciones y cronología.")
    
    with tab_refleja:
        st.markdown("""
    **Teoría Refleja (Reflex Theory)**  
    
    **Cronología:**
    Finales del siglo XIX y principios del siglo XX. Sir Charles Sherrington escribió la base experimental de esta teoría en 1906. Esta visión persistió sin ser cuestionada por muchos clínicos durante 50 años.

    **Postulados Principales:**  
    - Los reflejos son los bloques de construcción (building blocks) del comportamiento complejo.  
    - El comportamiento complejo se explica a través de la acción combinada de reflejos individuales encadenados (chained together).  
    - La estructura básica de un reflejo consiste en un receptor, un conductor y un efector (músculo).

    **Limitaciones:**  
    - No puede considerarse la unidad básica del comportamiento si se reconocen los movimientos espontáneos y voluntarios, ya que el reflejo debe ser activado por un agente externo.  
    - No explica adecuadamente el movimiento que ocurre en ausencia de un estímulo sensorial.  
    - No explica los movimientos rápidos (secuencias de movimientos que ocurren demasiado rápido para que la retroalimentación sensorial del movimiento precedente desencadene el siguiente).  
    - El concepto de encadenamiento de reflejos no explica la capacidad de producir movimientos novedosos.
        """)

    with tab_jerarquica:
        st.markdown("""
    **Teoría Jerárquica (Hierarchical Theory)**  
    
    **Cronología:**
    Principios a mediados del siglo XX. Hughlings Jackson argumentó que el cerebro tenía niveles de control superior, medio e inferior. Rudolf Magnus exploró reflejos en los años 1920, y Georg Schaltenbrand (1928) y Stephan Weisz (1938) aplicaron estos conceptos al desarrollo y el equilibrio. Investigadores como Arnold Gesell (1940s) y Myrtle McGraw (1945) describieron la maduración motora bajo este marco (Teoría Neuromaduracional).

    **Postulados Principales:**  
    - El sistema nervioso está organizado como una jerarquía.  
    - El control organizacional es de arriba hacia abajo (top down): cada nivel sucesivamente superior ejerce control sobre el nivel inferior. En una jerarquía vertical estricta, no hay control de abajo hacia arriba.  
    - Los centros superiores normalmente inhiben los centros reflejos inferiores.  
    - La teoría Reflejo/Jerárquica sugiere que el control motor surge de reflejos que están anidados dentro de niveles del SNC organizados jerárquicamente.  
    - La maduración normal del motor se atribuye a una creciente corticalización del SNC, lo que resulta en la emergencia de niveles de control superiores sobre reflejos de nivel inferior.

    **Limitaciones:**  
    - No puede explicar el dominio del comportamiento reflejo en ciertas situaciones en adultos normales (por ejemplo, pisar un alfiler resulta en control de abajo hacia arriba o bottom-up control).
        """)

    with tab_pm:
        st.markdown("""
    **Teorías de Programación Motora (Motor Programming Theories)**  
    
    **Cronología:**
    Mediados del siglo XX (los científicos que contribuyeron incluyen a Bernstein, 1967; Keele, 1968; Wilson, 1961). Experimentos a principios de los años 1960 (saltamontes/langosta) apoyaron esta visión.

    **Postulados Principales:**  
    - Se enfocan en la fisiología de las acciones en lugar de las reacciones.  
    - Un concepto clave es el patrón motor central (o programa motor), el cual es más flexible que el reflejo porque puede ser activado tanto por estímulos sensoriales como por procesos centrales.  
    - El movimiento es posible en ausencia de acción refleja.  
    - El término programa motor puede usarse para identificar un Generador de Patrón Central (CPG), un circuito neural específico, estereotipado y cableado (como el que genera la marcha).  
    - El término también describe programas motores de alto nivel que almacenan las reglas abstractas para generar movimientos. Estas reglas permiten realizar la tarea con una variedad de sistemas efectores (por ejemplo, escribir la firma con la mano o con la boca mantiene los elementos constantes del patrón).

    **Limitaciones:**  
    - Un programa motor central no puede considerarse el único determinante de la acción.  
    - No tiene en cuenta que el sistema nervioso debe lidiar con variables musculoesqueléticas y ambientales (como la gravedad, la inercia o la fatiga muscular) al lograr el control del movimiento.
        """)

    with tab_sistemas:
        st.markdown("""
    **Teoría de Sistemas (Systems Theory)**  
    
    **Cronología:**
    Principios y mediados del siglo XX. Nicolai Bernstein (1896–1966) fue un científico ruso que comenzó a desarrollar esta perspectiva.

    **Postulados Principales:**  
    - No se puede entender el control neural del movimiento sin comprender las características del sistema que se mueve (el cuerpo) y las fuerzas externas e internas que actúan sobre él (gravedad, inercia).  
    - El cuerpo es visto como un sistema mecánico.  
    - El mismo comando central puede resultar en movimientos muy diferentes debido a la interacción entre fuerzas externas y variaciones en las condiciones iniciales.  
    - Un desafío clave es el problema de los grados de libertad redundantes. La coordinación del movimiento es el proceso de dominar estos grados de libertad.  
    - Como solución, Bernstein hipotetizó que los niveles superiores del sistema nervioso activan niveles inferiores que, a su vez, activan sinergias (grupos de músculos que se ven obligados a actuar juntos como una unidad).  
    - El control del movimiento integrado está probablemente distribuido a través de muchos sistemas interactuantes que trabajan cooperativamente.
        """)

    with tab_dinamicos:
        st.markdown("""
    **Teoría de Sistemas Dinámicos (Dynamic Systems Theory)**  
    
    **Cronología:**
    Desde la propuesta inicial de Bernstein. Es una expansión de la Teoría de Sistemas y a menudo se utilizan los términos indistintamente.

    **Postulados Principales:**  
    - El movimiento es una propiedad emergente. Emerge de la interacción de múltiples elementos que se autoorganizan (self-organization) basándose en propiedades dinámicas, sin necesidad de comandos o programas motores de un centro superior.  
    - Muestra propiedades no lineales: el resultado no es proporcional a la entrada. Un pequeño cambio en un parámetro puede provocar una transformación en el comportamiento (ejemplo: al aumentar la velocidad lineal, un animal pasa repentinamente de caminar a trotar).  
    - Introduce el concepto de parámetro de control, una variable que regula el cambio en el comportamiento de todo el sistema (ejemplo: la velocidad en la transición de la marcha).  
    - La variabilidad inherente en el movimiento humano es crítica para la función óptima (no es vista como un error, a diferencia de otras teorías).  
    - Un estado atractor es un patrón de movimiento preferido y altamente estable.

    **Limitaciones:**  
    - La limitación de algunas variaciones de este modelo es la presunción de que el sistema nervioso tiene un papel menos importante en la determinación del comportamiento, dando un papel más dominante a las fórmulas matemáticas y los principios de la mecánica corporal.
        """)

    with tab_ecologica:
        st.markdown("""
    **Teoría Ecológica (Ecological Theory)**  
    
    **Cronología:**
    Los años 1960. James Gibson comenzó a explorar cómo los sistemas motores interactúan con el entorno para el comportamiento orientado a objetivos. Sus estudiantes la expandieron, llamándola enfoque ecológico.

    **Postulados Principales:**  
    - El control motor evolucionó para que los animales pudieran afrontar el entorno, moviéndose eficazmente para alcanzar metas (ejemplo: encontrar comida).  
    - Se centra en cómo detectamos la información relevante en el entorno para la acción.  
    - El organismo es visto como un sistema de percepción/acción que explora activamente el entorno, no como un sistema sensorial/motor reactivo.  
    - La organización de la acción es específica de la tarea y del entorno en el que se realiza.  
    - La percepción se enfoca en detectar la información ambiental que sustentará las acciones necesarias para lograr el objetivo.

    **Limitaciones:**  
    - Ha tendido a dar menos énfasis a la organización y función del sistema nervioso que conduce a esta interacción, cambiando el énfasis de la investigación del sistema nervioso a la interfaz organismo/entorno.
        """)

    
    st.markdown("---")
    st.markdown("### Perspectivas actuales")
    st.markdown("#### Hipótesis del descontrol múltiple (UCM)")


    def crear_plot_sinergia_ucm(title: str, synergy: bool = True, n_points: int = 24, valor_deseado = 10):
    
        np.random.seed(42)  # reproducibilidad
        puntos_size = 5
        
        if synergy:
            # A synergy → puntos alineados a lo largo de la UCM
            x = np.random.uniform(2, 8, n_points)
            y = -x + valor_deseado + np.random.normal(0, 0.8, n_points)
            subtitle = "Es sinergia"
        else:
            # Not a synergy → dispersión aleatoria, relación VarUCM/VarORT < 1
            x = np.random.uniform(2, 8, n_points)
            y = np.random.uniform(2, 8, n_points)
            subtitle = "No es sinergia"
        
        fig = go.Figure()
        
        # Puntos
        fig.add_trace(go.Scatter(
            x=x, y=y,
            mode="markers",
            marker=dict(color="#CCA525", size=puntos_size),  # naranjo pastel sin contorno
            showlegend=False
        ))
        
        # Línea Var UCM
        fig.add_trace(go.Scatter(
            x=[0, 10], 
            y=[10, 0],
            mode="lines",
            line=dict(color="white", dash="dash", width=2),
            name="VarUCM"
        ))

        # Línea Var ORT
        fig.add_trace(go.Scatter(
            x=[0, 10], 
            y=[0, 10],
            mode="lines",
            line=dict(color="white", dash="dash", width=2),
            name="VarORT"
        ))

        # ----- Elipse IC95% -----
        cov = np.cov(x, y)
        mean_x, mean_y = np.mean(x), np.mean(y)
        chi2_val = chi2.ppf(0.95, df=2)  # IC95%
        
        theta = np.linspace(0, 2*np.pi, 100)
        circle = np.array([np.cos(theta), np.sin(theta)])  # círculo unitario
        vals, vecs = np.linalg.eigh(cov)
        ellipse = vecs @ np.diag(np.sqrt(vals * chi2_val)) @ circle
        ellipse[0, :] += mean_x
        ellipse[1, :] += mean_y
        
        fig.add_trace(go.Scatter(
            x=ellipse[0, :],
            y=ellipse[1, :],
            mode="lines",
            line=dict(color="rgba(204,197,37,0.7)", width=2),  # naranjo pastel
            fill="toself",
            fillcolor="rgba(204,197,37,0.2)",  # mismo naranjo pastel alpha=0.4
            showlegend=False
        ))

        # Layout
        fig.update_layout(
            title=dict(text=f"{subtitle}", x=0.5, xanchor="center"),
            xaxis=dict(
                range=[0, 12],
                showgrid=False,
                zeroline=False,
                color="white",
                showline=True,
                linewidth=2,
                linecolor="white",
                scaleanchor="y",
                scaleratio=1,
                fixedrange=True  # no zoom
            ),
            yaxis=dict(
                range=[0, 12],
                showgrid=False,
                zeroline=False,
                color="white",
                showline=True,
                linewidth=2,
                linecolor="white",
                scaleanchor="x",
                scaleratio=1,
                fixedrange=True  # no zoom
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            legend=dict(font=dict(color="white"))
        )
        
        return fig


    # ---- Uso en Streamlit ----
    col1, col2 = st.columns(2)
    
    with col1:
        st.plotly_chart(crear_plot_sinergia_ucm(title="Not a synergy", synergy=False), 
                        use_container_width=True,
                        config={"staticPlot": True}
                        )
    
    with col2:
        st.plotly_chart(crear_plot_sinergia_ucm(title="A synergy", synergy=True), 
                        use_container_width=True,
                        config={"staticPlot": True}
                        )
