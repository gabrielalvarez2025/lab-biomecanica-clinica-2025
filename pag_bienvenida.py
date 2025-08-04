import streamlit as st

def mostrar():
    
    st.info("⬅ Usa el menú lateral para navegar por las secciones que estén disponibles.")
    
    # Título principal
    st.title("Espacio Interactivo LabBC")
    st.subheader("**Análisis Biomecánico del Movimiento**")

    st.markdown("Estimado/a estudiante. "
                "Bienvenido/a a este espacio interactivo del curso de Análisis Biomecánico del Movimiento. " \
                "Aquí encontrarás recursos y herramientas interactivas para complementar tu aprendizaje."
                )
    st.info("⬅ Usa el menú lateral para navegar por las secciones que estén disponibles.")
    st.markdown("---")
    
    st.title("Te damos la Bienvenida 👋")
    st.write("Usa el menú de la izquierda para navegar.")

    # Unidades del curso
    st.markdown("""
    A continuación, te presentamos una visión general de las **unidades** que abordaremos:            
    
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