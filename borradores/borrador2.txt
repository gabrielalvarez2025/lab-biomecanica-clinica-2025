import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(page_title="Bienvenida - Análisis Biomecánico del Movimiento", layout="centered")



# Título principal
st.title("Espacio Interactivo LabBC")
st.subheader("**Análisis Biomecánico del Movimiento**")

st.markdown("Estimado/a estudiante. "
            "Bienvenido/a a este espacio interactivo del curso de Análisis Biomecánico del Movimiento. " \
            "Aquí encontrarás recursos y herramientas interactivas para complementar tu aprendizaje."
            )
st.info("⬅ Usa el menú lateral para navegar por las secciones que estén disponibles.")
st.markdown("---")

# Nombres de las páginas
pag_bienvenida          = "Bienvenida"
pag_introduccion        = "Sección 1: Introducción"
pag_bioinstrumentacion  = "Sección 2: Bioinstrumentación"
pag_control_motor       = "Sección 3: Teorías del control motor"
pag_balance             = "Sección 4: Sistema sensoriomotor y balance"
pag_marcha              = "Sección 5: Análisis de marcha"


# Sidebar con selector de página

# Sidebar instrucción
st.sidebar.markdown("Selecciona una sección:")  # línea horizontal para separar

# Sidebar 1
sidebar1 = st.sidebar.radio("Página principal del espacio interactivo", [
    pag_bienvenida,
    
])

#st.sidebar.markdown("---")  # línea horizontal para separar

# Sidebar 2
sidebar2 = st.sidebar.radio("Para comenzar:", [
    pag_introduccion
])

#st.sidebar.markdown("---")  # línea horizontal para separar

# Sidebar 3: Unidad 1
sidebar3 = st.sidebar.radio("Unidad 1:", [
    pag_bioinstrumentacion,
    pag_control_motor,
    pag_balance,
    pag_marcha
])

#st.sidebar.markdown("---")  # línea horizontal para separar

# Sidebar: Unidad 2
sidebar4 = st.sidebar.radio("Unidad 2:", [
    pag_control_motor,
    pag_balance,
    pag_marcha
])

#st.sidebar.markdown("---")  # línea horizontal para separar

# Sidebar: Unidad 3
sidebar5 = st.sidebar.radio("Unidad 3:", [
    pag_marcha
])

# Para decidir qué mostrar combinando la selección de ambos radios
if sidebar1:
    pagina_seleccionada = sidebar1
elif sidebar2:
    pagina_seleccionada = sidebar2
elif sidebar3:
    pagina_seleccionada = sidebar3
elif sidebar4:
    pagina_seleccionada = sidebar4
elif sidebar5:
    pagina_seleccionada = sidebar5



# Mostrar contenido según la selección
if pagina_seleccionada == pag_bienvenida:
    st.title("Te damos la Bienvenida 👋")
    st.write("Usa el menú de la izquierda para navegar.")

elif pagina_seleccionada == pag_introduccion:
    st.header("📘 Unidad 1: Introducción al análisis del movimiento")
    st.markdown("- Etapas del análisis\n- Cinemática\n- Cinética")

elif pagina_seleccionada == pag_bioinstrumentacion:
    st.header("🧪 Unidad 2: Bioinstrumentación")
    st.markdown("- Electromiografía (EMG)\n- Plataforma de fuerza\n- Videofotogrametría\n- Goniometría")

elif pagina_seleccionada == pag_control_motor:
    st.header("🧠 Unidad 3: Teorías del control motor")
    st.markdown("- Teorías antiguas\n- Teoría de sistemas dinámicos\n- Teoría de modelos internos")

elif pagina_seleccionada == pag_balance:
    st.header("⚖️ Unidad 4: Sistema sensoriomotor y balance")

elif pagina_seleccionada == pag_marcha:
    st.header("🚶 Unidad 5: Análisis de marcha")

# Mensaje de bienvenida
st.markdown("""
¡Hola! Este espacio está diseñado para acompañarte a lo largo del curso.  
Aquí encontrarás visualizaciones, animaciones y herramientas interactivas para reforzar los contenidos.
            
Esta es una herramienta que recién estamos desarrollando, por lo que es posible que veas bastantes cambios durante el semestre, mientras aprendemos a perfeccionarla.

A continuación, te presentamos una visión general de las **unidades** que abordaremos:
""")


