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
from instrucciones_opencap import instrucciones as mostrar_instrucciones_opencap



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
    pag_marcha
    pag_instrucciones_opencap
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

elif pagina == pag_instrucciones_opencap:
    mostrar_instrucciones_opencap()