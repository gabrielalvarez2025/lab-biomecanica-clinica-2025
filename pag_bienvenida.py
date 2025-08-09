import streamlit as st

def mostrar(boolean=True):
    if boolean:
        main()
    else:
        st.write("Esta sección está en construcción :)")

def main():
    
    # Título principal
    st.title("Espacio Interactivo LabBC")
    st.subheader("**Análisis Biomecánico del Movimiento**")

    # Mensaje de bienvenida
    st.markdown("Estimado/a estudiante. "
                "Bienvenido/a a este espacio interactivo del curso de Análisis Biomecánico del Movimiento. " \
                "Aquí encontrarás recursos y herramientas interactivas para complementar tu aprendizaje."
                )
    
    # Mensaje aclaración
    st.markdown("""
    ¡Hola! Este espacio está diseñado para acompañarte a lo largo del curso.  
    Aquí encontrarás visualizaciones, animaciones y herramientas interactivas para reforzar los contenidos.
                
    Esta es una herramienta que recién estamos desarrollando, por lo que es posible que veas bastantes cambios durante el semestre, mientras aprendemos a perfeccionarla.

    """)

    # Sobre barra lateral
    st.write("Usa el menú de la izquierda para navegar.")
    st.info("⬅ Usa el menú lateral para navegar por las secciones que estén disponibles.")
    
    st.markdown("---")
    
    st.title("Te damos la Bienvenida 👋")
    

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