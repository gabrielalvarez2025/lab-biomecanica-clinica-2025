import streamlit as st
import matplotlib.pyplot as plt
import numpy as np


st.set_page_config(page_title="Bienvenida - Análisis Biomecánico del Movimiento", layout="centered")



# Título principal
st.title("Espacio Interactivo LabBC")
st.subheader("**Análisis Biomecánico del Movimiento**")

st.markdown("Estimado/a estudiante. "
            "Bienvenido/a a este espacio interactivo del curso de Análisis Biomecánico del Movimiento." \
            "Aquí encontrarás recursos y herramientas interactivas para complementar tu aprendizaje."
            "---")

st.info("⬅ Usa el menú lateral para navegar por las unidades cuando estén disponibles.")




# Sidebar con selector de página
pagina = st.sidebar.radio("Selecciona una sección:", [
    "Bienvenida",
    "Unidad 1: Introducción",
    "Unidad 2: Bioinstrumentación",
    "Unidad 3: Teorías del control motor",
    "Unidad 4: Sistema sensoriomotor y balance",
    "Unidad 5: Análisis de marcha"
])

# Mostrar contenido según la selección
if pagina == "Bienvenida":
    st.title("Te damos la Bienvenida 👋")
    st.write("Usa el menú de la izquierda para navegar.")




elif pagina == "Unidad 1: Introducción":
    st.header("📘 Unidad 1: Introducción al análisis del movimiento")
    st.markdown("- Etapas del análisis\n- Cinemática\n- Cinética")

elif pagina == "Unidad 2: Bioinstrumentación":
    st.header("🧪 Unidad 2: Bioinstrumentación")
    st.markdown("- Electromiografía (EMG)\n- Plataforma de fuerza\n- Videofotogrametría\n- Goniometría")

elif pagina == "Unidad 3: Teorías del control motor":
    st.header("🧠 Unidad 3: Teorías del control motor")
    st.markdown("- Teorías antiguas\n- Teoría de sistemas dinámicos\n- Teoría de modelos internos")

elif pagina == "Unidad 4: Sistema sensoriomotor y balance":
    st.header("⚖️ Unidad 4: Sistema sensoriomotor y balance")

elif pagina == "Unidad 5: Análisis de marcha":
    st.header("🚶 Unidad 5: Análisis de marcha")

# Mensaje de bienvenida
st.markdown("""
¡Hola! Este espacio está diseñado para acompañarte a lo largo del curso.  
Aquí encontrarás visualizaciones, animaciones y herramientas interactivas para reforzar los contenidos.
            
Esta es una herramienta que recién estamos desarrollando, por lo que es posible que veas bastantes cambios durante el semestre, mientras aprendemos a perfeccionarla.

A continuación, te presentamos una visión general de las **unidades** que abordaremos:
""")


# Unidades del curso
st.markdown("""
### Unidades del curso

1. **Introducción al análisis del movimiento**
   - Etapas del análisis
   - Cinemática
   - Cinética

2. **Bioinstrumentación**
   - Electromiografía (EMG)
   - Plataforma de fuerza
   - Videofotogrametría
   - Goniometría

3. **Teorías del control motor**
   - Teorías antiguas
   - Teoría de sistemas dinámicos
   - Teoría de modelos internos

4. **Sistema sensoriomotor y balance**

5. **Análisis de marcha**
""")

st.markdown("---")

