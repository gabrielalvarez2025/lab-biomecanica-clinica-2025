import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# importar secciones
from pag_bienvenida import main_bienvenida
from pag_introduccion import main_introduccion
from pag_bioinstrumentacion import main_bioinstrumentacion
from pag_control_motor import main_control_motor
from pag_balance import main_balance
from pag_marcha import main_marcha
from instrucciones_opencap import main_instrucciones_opencap


def mostrar(func, mostrar: bool = True):
    """
    Función para mostrar una página a través de su función func=main().
    Si mostrar=True, se muestra el contenido; si False, muestra mensaje de "en construcción".

    **func**: función que contiene el contenido de la página.
    **mostrar**: booleano que indica si se debe mostrar el contenido o no.
    
    """
    if mostrar:
        func()
    else:
        st.markdown("## Esta sección está en construcción :)")
        st.image("images/img_gears.gif")  # Imagen de engranajes animados

# Configuración de la página
st.set_page_config(page_title="Espacio LabBC", layout="centered", initial_sidebar_state="expanded")



# Nombres de las páginas
pag_bienvenida          = "Bienvenida"
pag_introduccion        = "Introducción"
pag_bioinstrumentacion  = "Bioinstrumentación"
pag_control_motor       = "Teorías del control motor"
pag_balance             = "Sistema sensoriomotor y balance"
pag_marcha              = "Análisis de marcha"

# Paginas adicionales
pag_instrucciones_opencap = "Instrucciones OpenCap"




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
    pag_marcha,
    pag_instrucciones_opencap
])

st.sidebar.markdown("---")  # línea horizontal para separar





# Mostrar contenido según la selección
if pagina == pag_bienvenida:
    mostrar(main_bienvenida, True)

elif pagina == pag_introduccion:
    mostrar(main_introduccion, True)

elif pagina == pag_bioinstrumentacion:
    mostrar(main_bioinstrumentacion, False)

elif pagina == pag_control_motor:
    mostrar(main_control_motor, False)

elif pagina == pag_balance:
    mostrar(main_balance, False)

elif pagina == pag_marcha:
    mostrar(main_marcha, False)

elif pagina == pag_instrucciones_opencap:
    mostrar(main_instrucciones_opencap, True)