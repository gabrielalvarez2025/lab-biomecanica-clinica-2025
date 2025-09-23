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


    def crear_plot_sinergia_ucm(
        n_points: int = 24,
        valor_deseado: float = 10,
        mostrar_numeros: bool = True,
        mostrar_elipse: bool = True,
        var_ucm: float = 1,
        var_ort: float = 1,
        dof_x: str = "Grado de libertad A<br>(por ej. Fuerza mano izquierda)",
        dof_y: str = "Grado de libertad A<br>(por ej. Fuerza mano derecha)"
    ):
        np.random.seed(42)
        puntos_size = 5

        if var_ort == 0.0:
            var_ort = 0.000000001
            ratio_var = "♾️"
        else:
            ratio_var = round((var_ucm / var_ort), 2)

        largo_max_ejes = np.sqrt(2 * valor_deseado**2)

        eje_ucm = var_ucm * largo_max_ejes
        eje_ort = var_ort * largo_max_ejes


        

        

        

            
        

        # ----- Rotación 45° (VarUCM alineada con y=-x+valor_deseado) -----
        theta_rot = np.pi / 4 * 3
        R = np.array([[np.cos(theta_rot), -np.sin(theta_rot)],
                    [np.sin(theta_rot),  np.cos(theta_rot)]])

        # ----- Dibujar elipse -----
        t = np.linspace(0, 2*np.pi, 100)
        x_ellipse = (eje_ucm/2) * np.cos(t)
        y_ellipse = (eje_ort/2) * np.sin(t)
        ellipse_coords = R @ np.array([x_ellipse, y_ellipse])
        
        # Centrar en medio del plot
        x_center, y_center = valor_deseado / 2, valor_deseado / 2
        x_ellipse_rot = ellipse_coords[0, :] + x_center
        y_ellipse_rot = ellipse_coords[1, :] + y_center

        # ----- Distribuir puntos aleatorios dentro de la elipse -----
        points_x, points_y = [], []
        while len(points_x) < n_points:
            x_rand = np.random.uniform(-(eje_ucm/2), (eje_ucm/2))
            y_rand = np.random.uniform(-(eje_ort/2), (eje_ort/2))
            if (x_rand/(eje_ucm/2))**2 + (y_rand/(eje_ort/2))**2 <= 1:
                # Rotar y centrar
                pt_rot = R @ np.array([[x_rand], [y_rand]])
                points_x.append(pt_rot[0,0] + x_center)
                points_y.append(pt_rot[1,0] + y_center)

        if (var_ucm / var_ort) > 1: # si es sinergia
            subtitle = f'Es sinergia (ratio = {ratio_var})'
        else:
            subtitle = f'No es sinergia (ratio = {ratio_var})'
            # else if (var_ucm / var_ort) <=1, no es sinergia

        
        
        

        fig = go.Figure()

        if mostrar_elipse:
            # ----- Elipse -----
            fig.add_trace(go.Scatter(
                x=x_ellipse_rot,
                y=y_ellipse_rot,
                mode="lines",
                line=dict(color="#3C3718", width=1),
                fill="toself",
                fillcolor="rgba(204,197,37,0.05)",
                showlegend=False
            ))

        

        # ----- Líneas VarUCM y VarORT -----
        fig.add_trace(go.Scatter(
            x=[0, valor_deseado],
            y=[valor_deseado, 0],
            mode="lines",
            line=dict(color="#45A2A2", dash="dash"),
            name="Var<sub>UCM</sub>"
        ))
        fig.add_trace(go.Scatter(
            x=[0, valor_deseado],
            y=[0, valor_deseado],
            mode="lines",
            line=dict(color="#D54341", dash="dash"),
            name="Var<sub>ORT</sub>"
        ))

        # ----- Puntos -----
        fig.add_trace(go.Scatter(
            x=points_x,
            y=points_y,
            mode="markers",
            marker=dict(color="#D7AD17", size=puntos_size),
            showlegend=False
        ))

        # ----- Layout -----
        fig.update_layout(
            title=dict(text=subtitle, x=0.5, y=0.9, xanchor="center"),
            xaxis=dict(
                title=dof_x,
                range=[0, valor_deseado],
                showgrid=False,
                showline=True,
                linecolor="white",
                linewidth=2,
                fixedrange=True,
                scaleanchor="y",
                scaleratio=1,
                showticklabels=mostrar_numeros
            ),
            yaxis=dict(
                title=dof_y,
                range=[0, valor_deseado],
                showgrid=False,
                showline=True,
                linecolor="white",
                linewidth=2,
                fixedrange=True,
                scaleanchor="x",
                scaleratio=1,
                showticklabels=mostrar_numeros
            ),
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            legend=dict(
                orientation="v",
                y=1.0,
                x=0.5,
                xanchor="left",
                yanchor="top",
                font=dict(color="white"),
                bgcolor="rgba(0,0,0,0)"
            )
        )

        return fig

    st.markdown("Cuando tratamos de realizar una tarea motora, el sistema nervioso lidia con una gran cantidad de grados de libertad (muchos músculos, articulaciones, segmentos corporales, etc. que pueden moverse de muchas maneras diferentes). Algunas combinaciones de estos grados de libertad resultan en outcomes exitosos para lo que queremos lograr; otros llevan a outcomes fallidos.")
    st.markdown("Uno de los grandes problemas del control motor es entender cómo el sistema nervioso maneja esta gran cantidad de alternativas para realizar una misma tarea y selecciona una combinación adecuada de grados de libertad para lograr el objetivo de forma exitosa.")

    st.markdown("La hipótesis del manifold no-controlado (uncontrolled manifold hypothesis, UCM) propone que el sistema nervioso organiza los grados de libertad en sinergias funcionales que estabilizan las variables de desempeño que son relevantes para la tarea (por ejemplo, la posición de la mano al alcanzar un objeto).")
    st.markdown("Una sinergia es un conjunto de elementos del sistema que están vinculados para actuar como una unidad funcional. Las sinergias permiten que el sistema nervioso controle múltiples grados de libertad. Al coordinar estos elementos, las sinergias logran reducir la complejidad del control y estabilizar alguna variable de desempeño.")

    st.markdown("Cada vez que realizas un movimiento, mediado por dos elementos con el potencial de formar una sinergia, los grados de libertad pueden hacer variar el resultado de la tarea. Por ejemplo, si consideramos la articulación del codo y del hombro al hacer un lanzamiento de básquet, hay muchas combinaciones posibles de ángulos de codo y hombro que pueden llevar a que el balón sea lanzado con éxito. Algunas combinaciones pueden ser más precisas que otras.")

    st.markdown("En la hipótesis UCM, las variaciones en los grados de libertad se dividen en dos componentes: ")


    esp1, col_plot, esp2 = st.columns([25, 50, 25])

    with col_plot:
        st.plotly_chart(crear_plot_sinergia_ucm(n_points=24, valor_deseado=10, mostrar_numeros=False,
                                                var_ucm=1, 
                                                var_ort=0), 
                        use_container_width=True,
                        config={"staticPlot": True}
                        )
        
        st.plotly_chart(crear_plot_sinergia_ucm(n_points=50, valor_deseado=10, mostrar_numeros=False, mostrar_elipse=False,
                                                var_ucm=0.7, 
                                                var_ort=0.7), 
                        use_container_width=True,
                        config={"staticPlot": True}
                        )
    
    
    # ---- Uso en Streamlit ----
    col1, esp, col2 = st.columns([0.49, 0.02, 0.49])
    
    with col1:
        
        # NO es sinergia (ratio <= 1)
        plot_no_sinergia = crear_plot_sinergia_ucm(mostrar_numeros=False, mostrar_elipse=1,
                                                   var_ucm=0.3,
                                                   var_ort=0.45
                                                   )
        
        st.plotly_chart(plot_no_sinergia, use_container_width=True, config={"staticPlot": True})
    
    with col2:
        
        # SÍ es sinergia (ratio > 1)
        plot_es_sinergia = crear_plot_sinergia_ucm(mostrar_numeros=False, mostrar_elipse=1,
                                                   var_ucm=0.8,
                                                   var_ort=0.2
                                                   )
        
        st.plotly_chart(plot_es_sinergia, use_container_width=True, config={"staticPlot": True})


    
    st.markdown(" ")
    st.markdown(" ")
    st.markdown("---")
    st.markdown(" ")
    
    col_sinergia_debil, esp_sinergias, col_sinergia_fuerte = st.columns([0.49, 0.02, 0.49])

    with col_sinergia_debil:
        
        st.markdown("##### Sinergia débil")

        plot_sinergia_debil = crear_plot_sinergia_ucm(mostrar_numeros=False, mostrar_elipse=1,
                                                   var_ucm=0.50,
                                                   var_ort=0.2
                                                   )
        
        st.plotly_chart(plot_sinergia_debil, use_container_width=True, config={"staticPlot": True})

    with col_sinergia_fuerte:
        
        st.markdown("##### Sinergia fuerte")

        plot_sinergia_fuerte = crear_plot_sinergia_ucm(mostrar_numeros=False, mostrar_elipse=1,
                                                   var_ucm=0.83,
                                                   var_ort=0.2
                                                   )
        
        st.plotly_chart(plot_sinergia_fuerte, use_container_width=True, config={"staticPlot": True})
    
    from streamlit.components.v1 import html

    
    lorem = (
    """
    <div style="color: white;">
        <p>Lorem Ipsum es simplemente el texto de relleno de las imprentas y archivos de texto. Lorem Ipsum ha sido el texto de relleno estándar de las industrias desde el año 1500, cuando un impresor (N. del T. persona que se dedica a la imprenta) desconocido usó una galería de textos y los mezcló de tal manera que logró hacer un libro de textos especimen. No sólo sobrevivió 500 años, sino que tambien ingresó como texto de relleno en documentos electrónicos, quedando esencialmente igual al original. Fue popularizado en los 60s con la creación de las hojas "Letraset", las cuales contenian pasajes de Lorem Ipsum, y más recientemente con software de autoedición, como por ejemplo Aldus PageMaker, el cual incluye versiones de Lorem Ipsum.</p>
        <p>Otro párrafo en blanco</p>
    </div>
    """
    * 50
    )
    
    st.markdown("---")
    html(lorem, height=500, scrolling=True)
    st.markdown("---")
    
