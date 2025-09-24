import streamlit as st
import matplotlib.pyplot as plt
import numpy as np
from streamlit_option_menu import option_menu


# importar secciones
from pag_bienvenida import main_bienvenida
from pag_introduccion import main_introduccion
from pag_bioinstrumentacion import main_bioinstrumentacion
from pag_control_motor import main_control_motor
from pag_balance import main_balance
from pag_marcha import main_marcha
from pag_opencap import main_opencap


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
pag_opencap = "Aplicando VFG: OpenCap"

selected = option_menu(
    None, 
    ["Home", "Upload", "Tasks", "QA", "Overall summary", "Settings"], 
    
    icons=['house', 'cloud-upload', "list-task", 'question-diamond-fill', 'card-list', 'gear'], 
    
    menu_icon="cast", 
    default_index=0, 
    orientation="horizontal",
    styles={
        "container": {"padding": "0!important", "background-color": "#fafafa"},
        "icon": {"color": "orange", "font-size": "25px"}, 
        "nav-link": {"font-size": "20px", "text-align": "center", "margin":"0px", "--hover-color": "#eee"},
        "nav-link-selected": {"background-color": "green"},
    }
)



# Sidebar con selector de página

# Sidebar instrucción
#st.sidebar.markdown("Selecciona una sección:")  # línea horizontal para separar

# Sidebar 1
pagina = st.sidebar.selectbox("Selecciona una sección:", [
    pag_bienvenida,
    pag_introduccion,
    pag_bioinstrumentacion,
    pag_control_motor,
    pag_balance,
    pag_marcha,
    pag_opencap
])




st.sidebar.markdown("---")  # línea horizontal para separar

# Leer parámetros de la URL
query_params = st.query_params
pagina_url = query_params.get("page", None)

if pagina_url == "bioinstrumentos":
    pagina = pag_bioinstrumentacion

if pagina_url == "opencap":
    st.header("Aplicando videofotogrametría con OpenCap")
    st.markdown("---")
    pagina = pag_opencap



# Mostrar contenido según la selección
if pagina == pag_bienvenida:
    mostrar(main_bienvenida, 1)

elif pagina == pag_introduccion:
    mostrar(main_introduccion, 1)

elif pagina == pag_bioinstrumentacion:
    mostrar(main_bioinstrumentacion, 1)

elif pagina == pag_control_motor:
    mostrar(main_control_motor, 1)

elif pagina == pag_balance:
    mostrar(main_balance, 1)

elif pagina == pag_marcha:
    mostrar(main_marcha, 1)

elif pagina == pag_opencap:
    st.header("Aplicando videofotogrametría con OpenCap")
    st.markdown("---")
    mostrar(main_opencap, True)