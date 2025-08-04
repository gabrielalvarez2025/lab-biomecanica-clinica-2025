import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# importar secciones
from pag_bienvenida import mostrar as mostrar_bienvenida
from pag_introduccion import mostrar as mostrar_introduccion
from pag_bioinstrumentacion import mostrar as mostrar_bioinstrumentacion
from pag_control_motor import mostrar as mostrar_control_motor
from pag_balance import mostrar as mostrar_balance
from pag_marcha import mostrar as mostrar_marcha




st.set_page_config(page_title="Bienvenida - Análisis Biomecánico del Movimiento", layout="centered")



# Nombres de las páginas
pag_bienvenida          = "Bienvenida"
pag_introduccion        = "Sección 1: Introducción"
pag_bioinstrumentacion  = "Sección 2: Bioinstrumentación"
pag_control_motor       = "Sección 3: Teorías del control motor"
pag_balance             = "Sección 4: Sistema sensoriomotor y balance"
pag_marcha              = "Sección 5: Análisis de marcha"


# Sidebar con selector de página

# Sidebar instrucción
#st.sidebar.markdown("Selecciona una sección:")  # línea horizontal para separar

# Sidebar 1
pagina = st.sidebar.radio("Selecciona una sección:", [
    pag_bienvenida,
    pag_introduccion,
    pag_bioinstrumentacion,
    pag_control_motor,
    pag_balance,
    pag_marcha
])

st.sidebar.markdown("---")  # línea horizontal para separar





# Mostrar contenido según la selección
if pagina == pag_bienvenida:
    mostrar_bienvenida()

elif pagina == pag_introduccion:
    mostrar_introduccion()

elif pagina == pag_bioinstrumentacion:
    mostrar_bioinstrumentacion()

elif pagina == pag_control_motor:
    mostrar_control_motor()

elif pagina == pag_balance:
    mostrar_balance()

elif pagina == pag_marcha:
    mostrar_marcha()

# Mensaje de bienvenida
st.markdown("""
¡Hola! Este espacio está diseñado para acompañarte a lo largo del curso.  
Aquí encontrarás visualizaciones, animaciones y herramientas interactivas para reforzar los contenidos.
            
Esta es una herramienta que recién estamos desarrollando, por lo que es posible que veas bastantes cambios durante el semestre, mientras aprendemos a perfeccionarla.

""")




