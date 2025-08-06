import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import random

def mostrar():
    st.header("Unidad 1: Bioinstrumentación")

    st.markdown(
        "- Electromiografía (EMG)\n"
        "- Plataforma de fuerza\n"
        "- Videofotogrametría\n"
        "- Goniometría"
    )

    sns.set_theme(style="darkgrid", palette="pastel")
    
    st.markdown("---")
    
    # Inicializar variable de sesión en False al principio
    if "mostrar_sumatoria" not in st.session_state:
        st.session_state["mostrar_sumatoria"] = False

    # Mostrar botones
    botones_tarjeta()

    # Mostrar contenido si fue activado
    if st.session_state["mostrar_sumatoria"]:
        play_emg_sumatoria()

    st.markdown("---")


def play_emg_sumatoria():
    
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
    esp1, col1, col2, esp2 = st.sidebar.columns([1, 2, 2, 1])  # proporciones


    with col1:
        if st.button("Reiniciar"):
            for i in range(num_ondas):
                st.session_state[f"amp_{i}"] = 1.0
                st.session_state[f"freq_{i}"] = 1.0
                st.session_state[f"fase_{i}"] = 0.0

    with col2:
        if st.button("Aleatorio"):
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
    st.markdown("---")

def botones_tarjeta():
    # CSS personalizado solo para el botón con id específico
    st.markdown("""
        <style>
        .custom-boton button {
            background-color: #f5f5f5;
            border: 1px solid #d3d3d3;
            padding: 30px 50px;
            border-radius: 12px;
            color: #233a3d;
            font-size: 18px;
            width: 100%;
            text-align: center;
            box-shadow: 2px 2px 8px rgba(0,0,0,0.1);
            transition: transform 0.1s ease-in-out;
            margin-top: 6px;
        }

        .custom-boton button:hover {
            background-color: #e0e0e0;
            transform: scale(1.05);
            cursor: pointer;
        }
        </style>
    """, unsafe_allow_html=True)

    # Columnas
    col1, col2 = st.columns(2)

    with col1:
        # Envolver el botón con una clase única
        with st.container():
            custom_btn = st.markdown('<div class="custom-boton">', unsafe_allow_html=True)
            if st.button("Sumatoria de ondas\n∑  ~𓂃〰️𓂃~"):
                st.session_state["mostrar_sumatoria"] = True
                st.success("¡Estás viendo la simulación de sumatoria de ondas!")
            st.markdown("</div>", unsafe_allow_html=True)

    with col2:
        st.markdown("""
            <p style="color: #dbdbdb; font-size: 16px; margin-top: 5px;">
            Si tienes dudas de por qué la señal de EMG tiene la forma que tiene o cuál es su relación con los potenciales de acción de unidades motoras (PAUMs), esta simulación te ayudará a entenderlo.
            </p>
        """, unsafe_allow_html=True)

    st.markdown("---")
    
    