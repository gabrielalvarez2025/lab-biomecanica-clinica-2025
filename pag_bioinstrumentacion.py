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

    
    
    # ELEMENTO INTERACTIVO: Descomposición de ondas
    st.subheader("Descomposición de ondas")

    st.markdown("""
    A continuación, puedes interactuar con una herramienta que simula la descomposición de una señal electromiográfica (EMG) en varias unidades motoras (UM).
    Esta herramienta te permite simular la descomposición de una señal EMG en varias unidades motoras (UM).
    
    
    """)

    st.info("⬅ En la barra lateral están los parámetros de cada onda.")

    st.markdown("""
    **Juega con ellos** para ajustar la amplitud, frecuencia y fase de cada onda y **mira cómo van cambiando su forma**:
                
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

    
    # ---------------------- Sliders de cada onda (generarlos) ----------------------

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
                        
                        Presiona **ALEATORIO** para establecer parámetros al azar para cada onda, o **REINICIAR** para volver a los valores default.
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

    
   

    # ---------------------- Sliders de cada onda (lectura) ----------------------
    
    # Leer sliders con los valores del session_state
    params = []
    for i in range(num_ondas):
        with st.sidebar.expander(f"Onda {i+1}", expanded=False):
            amp = st.slider(f"Amplitud (mV)", 0.0, float(amp_max), st.session_state[f"amp_{i}"], key=f"amp_{i}")
            freq = st.slider(f"Frecuencia (Hz)", 0.0, float(freq_max), st.session_state[f"freq_{i}"], key=f"freq_{i}")
            fase = st.slider(f"Fase", 0.0, float(fase_max), st.session_state[f"fase_{i}"], key=f"fase_{i}")
            params.append((amp, freq, fase))
    
     


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
        axs1[i].set_ylim(-amp_max, amp_max)
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

    st.write(f"""
                Las ondas individuales representan las unidades motoras (UM) que se suman para formar una señal EMG compuesta. Cuando las {n_ondas} ondas ocurren simultáneamente (chocan, se combinan), interfieren entre sí constructivamente en algunas zonas y destructivamente en otras.
                El resultado de sumar gráficamente esas {n_ondas} ondas que configuraste se muestra en la siguiente **onda resultante**:
    """)
    
    
    # Segunda figura: gráfico sumatoria total
    fig2, ax2 = plt.subplots(figsize=(10, 3))

    fig2.patch.set_alpha(0)
    ax2.patch.set_alpha(0)

    ax2.plot(x, suma_total, color='white')
    ax2.set_ylim(-amp_max * num_ondas, amp_max * num_ondas)
    ax2.set_ylabel("Amplitud", color='white', alpha=1)
    ax2.set_xlabel("Tiempo (ms)", color='white')
    ax2.set_title("Simulación de la onda resultante de la sumatoria", color='white')

    ax2.grid(True, alpha=0.10)
    ax2.tick_params(axis='x', colors='white')
    ax2.tick_params(axis='y', colors='white')

    st.pyplot(fig2)