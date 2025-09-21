import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.graph_objects as go
import random
import streamlit.components.v1 as components

from procesar_phyphox_acc import main_phyphox, ejemplo_fr_botas
from procesar_amti import main_forceplate
from pag_opencap import main_opencap
from procesar_delsys import main_delsys

def play_emg_sumatoria():
    
    st.markdown("---")
    sns.set_theme(style="darkgrid", palette="pastel")
    
    
    
    # ELEMENTO INTERACTIVO: Descomposición de ondas
    st.subheader("Sumatoria y descomposición de ondas")

    st.markdown("""
    A continuación, puedes interactuar con una herramienta que simula cómo varias ondas pueden sumarse entre sí para generar una nueva onda resultante, principio que (como veremos) es muy importante para entender cómo se genera la señal de electromiografía.
    """)

    st.info("⬅ En la barra lateral encontrarás botones y _sliders_ que te permitirán interactuar con la simulación.")
    
    st.markdown("Primero, selecciona el número de ondas que quieres simular. Te sugiero comenzar con 2.")
    # st.markdown("Luego, ajusta sus parámetros (amplitud, frecuencia y fase) y observa cómo estas se combinan para formar una onda resultante.")

    st.markdown("""
    **Juega con los botones** para ajustar la amplitud, frecuencia y fase de cada onda y **mira cómo van cambiando su forma**:
                
    """)

    # ---------------------- Configuración de sidebar del elemento interactivo ----------------------

    # Parámetros de la simulación, sidebar
    st.sidebar.title("Parámetros de simulación")
    num_ondas = st.sidebar.slider("Número de ondas", 1, 15, 2)
    
    # Parámetros maximos
    freq_max    = 100 # st.sidebar.slider("Frecuencia máxima (Hz)", 10, 100, 20)
    amp_max     = 2
    fase_max    = np.pi * 5

    x = np.linspace(0, 2 * np.pi, 500)
    suma_total = np.zeros_like(x)
    colores_pastel = sns.color_palette("pastel", num_ondas)    


    # ---------------------- Generar y configurar los sliders de cada onda (no mostrarlos) ----------------------

    # Sliders por onda
    # Inicializar session_state para cada parámetro si no existe o si cambió num_ondas
    for i in range(num_ondas):
        if f"amp_{i}" not in st.session_state or st.session_state.get("num_ondas_actual", None) != num_ondas:
            st.session_state[f"amp_{i}"] = 1.0
        if f"freq_{i}" not in st.session_state or st.session_state.get("num_ondas_actual", None) != num_ondas:
            st.session_state[f"freq_{i}"] = 1.0
        if f"fase_{i}" not in st.session_state or st.session_state.get("num_ondas_actual", None) != num_ondas:
            st.session_state[f"fase_{i}"] = 0.0
    
    st.session_state["num_ondas_actual"] = num_ondas

    # ---------------------- Botones de reinicio y aleatorio ----------------------
    
    # Instrucciones botones random y reiniciar
    st.sidebar.markdown("""
                        
                        Puedes presionar **ALEATORIO** para establecer parámetros al azar para cada onda. Presiona **REINICIAR** para volver a los valores iniciales.
                        """)
    
    
    # Configurar botones random y reiniciar en la sidebar
    esp1, col1, col2, esp2 = st.sidebar.columns([0.05, 0.45, 0.45, 0.05])  # proporciones


    with col1:
        if st.button("Reiniciar", key="boton_reiniciar"):
            for i in range(num_ondas):
                st.session_state[f"amp_{i}"] = 1.0
                st.session_state[f"freq_{i}"] = 1.0
                st.session_state[f"fase_{i}"] = 0.0

    with col2:
        if st.button("Aleatorio", key="boton_aleatorio"):
            for i in range(num_ondas):
                st.session_state[f"amp_{i}"] = random.uniform(0, amp_max)
                st.session_state[f"freq_{i}"] = random.uniform(0, freq_max)
                st.session_state[f"fase_{i}"] = random.uniform(0, fase_max)

    
   

    # ---------------------- Mostrar los sliders de cada onda ----------------------

    # Instrucciones
    st.sidebar.markdown("Cambia los parámetros de cada onda:")
    
    # Leer sliders con los valores del session_state
    params = []
    for i in range(num_ondas):
        with st.sidebar.expander(f"Onda {i+1}", expanded=False):
            amp = st.slider(f"Amplitud (mV)", 0.0, float(amp_max), st.session_state[f"amp_{i}"], key=f"amp_{i}")
            freq = st.slider(f"Frecuencia (Hz)", 0.0, float(freq_max), st.session_state[f"freq_{i}"], key=f"freq_{i}")
            fase = st.slider(f"Fase", 0.0, float(fase_max), st.session_state[f"fase_{i}"], key=f"fase_{i}")
            params.append((amp, freq, fase))
    

    # ---------------------- Graficar cada onda ----------------------
    
    # Primera figura: ondas individuales
    fig1, axs1 = plt.subplots(num_ondas, 1, figsize=(10, num_ondas * 1.5))

    fig1.patch.set_alpha(0)
    for ax in axs1:
        ax.patch.set_alpha(0)

        ax.grid(True, alpha=0.10)              # Grid con alpha=0.10
        ax.set_title(ax.get_ylabel(), color='white')  # Título blanco (usamos ylabel como título para cada plot)
        ax.set_ylabel(ax.get_ylabel(), color='white')
        ax.set_xlabel(ax.get_xlabel(), color='white')

        ax.tick_params(axis='x', colors='white')
        ax.tick_params(axis='y', colors='white')

    for i, (amp, freq, fase) in enumerate(params):
        y = amp * np.sin(2 * np.pi * freq * x + fase)
        suma_total += y
        axs1[i].plot(x, y, color=colores_pastel[i])
        axs1[i].set_ylim(-amp_max-0.5, amp_max+0.5)
        axs1[i].set_ylabel(f"Onda {i+1}", color='white')
        axs1[i].tick_params(axis='x', colors='white')
        axs1[i].grid(True, alpha=0.10)

        if i < num_ondas - 1:
            
            axs1[i].set_xticklabels([])               # pero oculta los números
            
        else:
            axs1[i].set_xlabel("Tiempo (ms)", color='white')
            axs1[i].tick_params(axis='x', colors='white')

    st.pyplot(fig1)

    # ---------------------- Texto pre - Onda Sumatoria ----------------------

    st.markdown(f"Cuando las {num_ondas} ondas ocurren simultáneamente (chocan, se combinan), interfieren entre sí constructivamente en algunas zonas y destructivamente en otras. Sus amplitudes se suman en cada instante de tiempo.")
    st.markdown(f"El resultado de sumar gráficamente esas {num_ondas} ondas que configuraste se muestra en la siguiente **onda resultante**:")
    
    
    # ---------------------- Graficar Onda Resultante ----------------------
    
    # Segunda figura: gráfico sumatoria total
    fig2, ax2 = plt.subplots(figsize=(10, 3))

    fig2.patch.set_alpha(0)
    ax2.patch.set_alpha(0)

    ax2.plot(x, suma_total, color='white')
    ax2.set_ylim((-amp_max * num_ondas)-0.5, (amp_max * num_ondas)+0.5)  # Ajustar el límite y para que se vea bien
    ax2.set_ylabel("Amplitud", color='white', alpha=1)
    ax2.set_xlabel("Tiempo (ms)", color='white')
    ax2.set_title("Simulación de la onda resultante de la sumatoria", color='white')

    ax2.grid(True, alpha=0.10)
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')

    st.pyplot(fig2)

    st.markdown(" ")

    st.subheader("Relación con la electromiografía")

    st.markdown("""
                La misma lógica anterior se aplica a la señal que vemos al tomar una **electromiografía (EMG)**. Esta señal también es una onda.
                
                La actividad eléctrica de cada unidad motora (UM) genera una onda eléctrica sencilla, como las ondas sinusoidales que configuraste arriba.
                Cada UM tiene una frecuencia de descarga y una amplitud distintas, por lo que cada onda es ligeramente diferente.
                Cuando estas ondas individuales se combinan, se suman para formar una señal EMG compuesta.

                Cuando el electrodo de superficie sensa la actividad eléctrica muscular, detecta la señal proveniente de varias UM cercanas al mismo tiempo (todas las que están bajo ese electrodo). 
                Por lo tanto, la señal EMG resultante que vemos en el computador es la que resulta de **sumar gráficamente todas las ondas individuales** provenientes de las distintas UM.
                
                Como la actividad de cada UM es ligeramente distinta (descargan a distintas frecuencias o se encuentran a diferentes profundidades) las ondas individuales no son iguales, sino que tienen distintas amplitudes, frecuencias y fases.
                
                Por lo tanto, la señal EMG resultante (con su forma "extraña" e irregular) es una **combinación de todas las ondas individuales**.
                Los potenciales de acción (PA) de muchas unidades motoras (UM) se suman para formar una señal EMG (lo que podrás encontrar en los textos como "PAUMs").
                
                """)
    #st.markdown("---")


def play_vfg_teorema_coseno():

    def generar_triangulo():
        """Genera lados válidos de un triángulo usando desigualdad triangular"""
        while True:
            a = random.uniform(2, 10)  # BC
            b = random.uniform(2, 10)  # AC
            c = random.uniform(2, 10)  # AB
            if a + b > c and a + c > b and b + c > a:
                return a, b, c

    def mostrar_valor(dato, valor):
        """Muestra '¿ ?' si el dato es el oculto, sino el valor con 2 decimales"""
        oculto = st.session_state.get("oculto", None)
        return "¿ ?" if dato == oculto else f"{valor:.2f}"



    st.set_page_config(layout="centered", initial_sidebar_state="expanded")
    st.title("Teorema del Coseno")

    # Inicializar estado
    if "lados" not in st.session_state:
        st.session_state.lados = generar_triangulo()
    if "oculto" not in st.session_state:
        st.session_state.oculto = random.choice(["a","b","c","α","β","γ"])

    # Botón para generar nuevo triángulo
    if st.button("🎲 Generar triángulo aleatorio"):
        st.session_state.lados = generar_triangulo()
        st.session_state.oculto = random.choice(["a","b","c","α","β","γ"])

    a, b, c = st.session_state.lados  # lados: a=BC, b=AC, c=AB

    # colores datos
    color_lado_a = "#FFB3BA"
    color_lado_b = "#BAE1FF"
    color_lado_c = "#BAFFC9"
    color_angulo_alfa = "#D62D9D"
    color_angulo_beta = "#8DA0C9"
    color_angulo_gamma = "#5EC073"

    # --- Construcción del triángulo ---
    A = np.array([0, 0])
    B = np.array([c, 0])
    x = (a**2 - b**2 + c**2) / (2*c)
    y = np.sqrt(max(a**2 - x**2, 0))
    C = np.array([x, y])

    fig = go.Figure()
    fig.add_trace(go.Scatter(
        x=[A[0], B[0], C[0], A[0]],
        y=[A[1], B[1], C[1], A[1]],
        mode='lines+markers',
        line=dict(color="white", width=3),
        marker=dict(size=12, color='green')
    ))

    # Función para desplazar etiquetas de lados hacia afuera
    def desplazar(p1, p2, d):
        v = np.array([p2[1]-p1[1], -(p2[0]-p1[0])])
        v = v / np.linalg.norm(v) if np.linalg.norm(v) > 0 else v
        return (p1 + p2)/2 + d*v

    offset = 0.6
    pos_a = ((B[0]+C[0])/2 + offset, (B[1]+C[1])/2) # lado a a la derecha
    pos_b = ((A[0]+C[0])/2 - offset, (A[1]+C[1])/2) # lado b a la izquierda
    pos_c = ((A[0]+B[0])/2, (A[1]+B[1])/2 - offset) # lado c hacia abajo

    fig.add_trace(go.Scatter(
        x=[pos_a[0], pos_b[0], pos_c[0]],
        y=[pos_a[1], pos_b[1], pos_c[1]],
        mode="text",
        text=[f"a", f"b", f"c"],
        textposition="middle center",
        textfont=dict(size=20, color=[color_lado_a, color_lado_b, color_lado_c]),
        showlegend=False
    ))

    max_coord = max(a, b, c) * 1.2
    fig.update_layout(
        width=500,
        height=500,
        xaxis=dict(range=[-1, max_coord], zeroline=False, showgrid=False, visible=False),
        yaxis=dict(range=[-1, max_coord], scaleanchor="x", zeroline=False, showgrid=False, visible=False),
        showlegend=False
    )

    # --- Cálculo de ángulos ---
    beta = np.degrees(np.arccos((b**2 + c**2 - a**2)/(2*b*c)))
    alpha = np.degrees(np.arccos((a**2 + c**2 - b**2)/(2*a*c)))
    gamma = np.degrees(np.arccos((a**2 + b**2 - c**2)/(2*a*b)))

    # Función para dibujar arcos
    def agregar_arco(fig, centro, ang_ini, ang_fin, radio=1, color="#FFB3BA"):
        theta = np.linspace(np.radians(ang_ini), np.radians(ang_fin), 30)
        x = centro[0] + radio * np.cos(theta)
        y = centro[1] + radio * np.sin(theta)
        x = np.append(x, centro[0])
        y = np.append(y, centro[1])
        fig.add_trace(go.Scatter(
            x=x, y=y, fill="toself",
            mode="lines", line_color=color,
            fillcolor=color, opacity=0.5,
            showlegend=False
        ))

    agregar_arco(fig, A, 0, alpha, color=color_angulo_alfa)
    agregar_arco(fig, B, 180-beta, 180, color=color_angulo_beta)
    ang_ini_C = np.degrees(np.arctan2(B[1]-C[1], B[0]-C[0]))
    agregar_arco(fig, C, ang_ini_C, ang_ini_C-gamma, color=color_angulo_gamma)

    # --- Mostrar datos y desafío ---
    col1, col2 = st.columns(2)
    oculto = st.session_state.oculto

    symbol_incognita = " __ "

    with col1:
        st.markdown(f"## Desafío:")
        st.markdown(f"Trata de calcular el dato **{oculto}** sabiendo que:")

        # Lados
        st.markdown("### Lados")
        st.markdown(f"• a = {symbol_incognita if oculto=='a' else f'{a:.2f}'}")
        st.markdown(f"• b = {symbol_incognita if oculto=='b' else f'{b:.2f}'}")
        st.markdown(f"• c = {symbol_incognita if oculto=='c' else f'{c:.2f}'}")

        # Ángulos
        st.markdown("### Ángulos")
        st.markdown(f"• α (en A) = {symbol_incognita if oculto=='α' else f'{alpha:.2f}°'}")
        st.markdown(f"• β (en B) = {symbol_incognita if oculto=='β' else f'{beta:.2f}°'}")
        st.markdown(f"• γ (en C) = {symbol_incognita if oculto=='γ' else f'{gamma:.2f}°'}")

    with col2:
        st.plotly_chart(fig, use_container_width=False)

    

    st.markdown(f"""
    <div style="text-align:center; font-size:30px; line-height:1.5;">
    
    <span style="color:{color_lado_c};">c</span><sup>2</sup> =
    <span style="color:{color_lado_a};">a</span><sup>2</sup> +
    <span style="color:{color_lado_b};">b</span><sup>2</sup> -
    2<span style="color:{color_lado_a};">a</span><span style="color:{color_lado_b};">b</span> · cos(<span style="color:{color_angulo_gamma};">γ</span>)
    </div>

    """, unsafe_allow_html=True)
    
    # Fórmula del coseno con dato oculto
    c_formula = symbol_incognita if oculto=='c' else 'c'
    a_formula = symbol_incognita if oculto=='a' else 'a'
    b_formula = symbol_incognita if oculto=='b' else 'b'
    gamma_formula = symbol_incognita if oculto=='γ' else 'γ'

    st.markdown(f"""
    <div style="text-align:center; font-size:30px; line-height:1.5;">
    <span style="color:{color_lado_c};">{c_formula}</span><sup>2</sup> =
    <span style="color:{color_lado_a};">{a_formula}</span><sup>2</sup> +
    <span style="color:{color_lado_b};">{b_formula}</span><sup>2</sup> -
    2<span style="color:{color_lado_a};">{a_formula}</span><span style="color:{color_lado_b};">{b_formula}</span> · cos(<span style="color:{color_angulo_gamma};">{gamma_formula}</span>)
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")


def presentar_botones_tarjeta():
    st.markdown("### **Elementos interactivos**")
    st.markdown("""
                En esta sección encontrarás elementos interactivos que te ayudarán a comprender mejor algunos de los conceptos relacionados a bioinstrumentación que vimos en clases.

                Presiona uno de los botones a continuación para activar el elemento interactivo que te interese revisar. Al presionar el botón una vez, se desplegará el elemento interactivo. Presiona nuevamente el botón para ocultarlo.
                """)
    st.empty()


def botones_tarjeta(nombre_estado, color_boton, color_parrafo, texto_boton, texto_parrafo):
    col1, col2 = st.columns([0.30, 0.70])

    with col1:
        altura_boton = 20
        font_size = 16

        color_fondo_base = color_boton
        color_fondo_hover = "#FFFFFF"
        color_fondo_active = "#0C8C1F"
        color_fuente_hover = "#2A2727"
        color_fuente_active = "#FFFFFF"
        color_fuente_parrafo = color_parrafo

        # CSS personalizado
        st.markdown(f"""
            <style>
                .big-button-container {{
                    display: flex;
                    align-items: stretch;
                    justify-content: center;
                    height: {altura_boton}px;
                    
                }}
                .big-button-container > div {{
                    width: 100%;
                }}
                div.stButton > button {{
                    width: 100%;
                    height: 100%;
                    min-height: {altura_boton}px;
                    border: 2px solid {color_fondo_base};
                    color: white;
                    background-color: {color_fondo_base};
                    font-weight: bold;
                    font-size: {font_size}px;
                    padding: 20px;
                    transition: 0.3s;
                }}
                div.stButton > button:hover {{
                    background-color: {color_fondo_hover};
                    border-color: {color_fondo_hover};
                    color: {color_fuente_hover};
                    cursor: pointer;
                }}
                div.stButton > button:active {{
                    background-color: {color_fondo_active};
                    color: {color_fuente_active};
                    border-color: {color_fondo_active};
                }}
            </style>
        """, unsafe_allow_html=True)

        if st.button(texto_boton, use_container_width=True):
            st.session_state[nombre_estado] = not st.session_state[nombre_estado]

    with col2:
        st.markdown(f"""
            <p style="font-size: 16px; margin-top: 10px; color: {color_fuente_parrafo};">
            {texto_parrafo}
            </p>
        """, unsafe_allow_html=True)


def main_bioinstrumentacion():
    
    

    st.header("Unidad 1: Bioinstrumentación")

    # Configuración tema seaborn
    sns.set_theme(style="darkgrid", palette="pastel")
    #st.set_page_config(layout="wide")

    
    

    
    # Fin listado de contenidos
    st.markdown("---")
    # Inicio de elementos interactivos

    # Inicialización segura SOLO una vez (para botones que usan session_state)
    if "mostrar_ejemplo_botas" not in st.session_state:
        st.session_state["mostrar_ejemplo_botas"] = False
    
    if "mostrar_sumatoria" not in st.session_state:
        st.session_state["mostrar_sumatoria"] = False
    
    if "mostrar_coseno" not in st.session_state:
        st.session_state["mostrar_coseno"] = False

    if "mostrar_torques" not in st.session_state:
        st.session_state["mostrar_torques"] = False

    if "mostrar_amti" not in st.session_state:
        st.session_state["mostrar_amti"] = False
    
    if "mostrar_delsys" not in st.session_state:
        st.session_state["mostrar_delsys"] = False

    if "mostrar_opencap" not in st.session_state:
        st.session_state["mostrar_opencap"] = False
    

    # colores lindos:
    #color_boton= "#368581", color_parrafo= "#89BBB8"
    #color_boton= "#81B238", color_parrafo= "#95E082"
    
    # Presentar botones tarjeta
    presentar_botones_tarjeta()

    tab_ejemplos, tab_simulaciones, tab_procesamiento = st.tabs([
        "Ejemplos de evaluación instrumentada",
        "Elementos interacivos para aprender",
        "Procesar datos reales"
    ])
    
    
    with tab_ejemplos:
        # Tarjeta 1: Ejemplo Botas
        parrafo_ejemplo_botas = "Aprende a medir la frecuencia respiratoria de un gato llamado Botas usando tu celular. Presiona el botón para ver un ejemplo de uso de instrumentos para complementar una evaluación clínica. "
        botones_tarjeta(nombre_estado="mostrar_ejemplo_botas",
                        texto_boton="Ejemplo 1: Midiendo la frecuencia respiratoria de un gato",
                        texto_parrafo=parrafo_ejemplo_botas,
                        color_boton= "#368581",
                        color_parrafo= "#89BBB8"
                        )
        
        # ✅ Mostrar contenido si fue activado
        if st.session_state["mostrar_ejemplo_botas"]:
            ejemplo_fr_botas()
        
    with tab_simulaciones:
        # Tarjeta 1: Sumatoria de PAUMs
        parrafo_sumatoria = "Si tienes dudas de por qué la señal de EMG tiene la forma que tiene o cuál es su relación con los potenciales de acción de unidades motoras <b>(PAUMs)</b>, esta simulación te ayudará a entenderlo."
        botones_tarjeta(nombre_estado="mostrar_sumatoria",
                        texto_boton="Sumatoria de ondas",
                        texto_parrafo=parrafo_sumatoria,
                        color_boton= "#368581",
                        color_parrafo= "#89BBB8"
                        )
        
        # Tarjeta 2: Teorema del coseno
        parrafo_coseno = "Si tienes dudas de por qué la señal de EMG tiene la forma que tiene o cuál es su relación con los potenciales de acción de unidades motoras <b>(PAUMs)</b>, esta simulación te ayudará a entenderlo."
        botones_tarjeta(nombre_estado="mostrar_coseno",
                        texto_boton="Practiquemos el teorema del coseno",
                        texto_parrafo=parrafo_coseno,
                        color_boton= "#368581",
                        color_parrafo= "#89BBB8"
                        )
        
        if st.session_state["mostrar_sumatoria"]:
            play_emg_sumatoria()
        
        if st.session_state["mostrar_coseno"]:
            play_vfg_teorema_coseno()
    
    with tab_procesamiento:
        # Tarjeta 3
        parrafo_interactivo2 = "Procesar datos de acelerometría tomados con el celular usando Phyphox"
        botones_tarjeta(nombre_estado="mostrar_torques",
                        texto_boton="Procesamiento de datos de acelerómetro con PhyPhox",
                        texto_parrafo=parrafo_interactivo2,
                        color_boton= "#368581",
                        color_parrafo= "#89BBB8"
                        )
        
        # Tarjeta 4
        parrafo_interactivo3 = "Procesar datos de la plataforma de fuerza del laboratorio (plataforma AMTI)"
        botones_tarjeta(nombre_estado="mostrar_amti",
                        texto_boton="Procesamiento de datos plataforma",
                        texto_parrafo=parrafo_interactivo3,
                        color_boton= "#368581",
                        color_parrafo= "#89BBB8"
                        )
        
        # Tarjeta 5
        parrafo_interactivo4 = "Procesar datos de EMG o IMU capturados con DELSYS"
        botones_tarjeta(nombre_estado="mostrar_delsys",
                        texto_boton="Procesamiento de datos Delsys",
                        texto_parrafo=parrafo_interactivo4,
                        color_boton= "#368581",
                        color_parrafo= "#89BBB8"
                        )
        
        # Tarjeta 6
        parrafo_interactivo5 = "Procesar datos de VFG capturados con OpenCap"
        botones_tarjeta(nombre_estado="mostrar_opencap",
                        texto_boton="Procesamiento de datos OpenCap",
                        texto_parrafo=parrafo_interactivo5,
                        color_boton= "#368581",
                        color_parrafo= "#89BBB8"
                        )
        
        if st.session_state["mostrar_torques"]:
            main_phyphox()
    
        if st.session_state["mostrar_amti"]:
            main_forceplate()
        
        if st.session_state["mostrar_delsys"]:
            main_delsys()

        if st.session_state["mostrar_opencap"]:
            st.markdown("---")
            main_opencap()
    
    
    
    

    
    
    
    
    


    st.markdown("---")

