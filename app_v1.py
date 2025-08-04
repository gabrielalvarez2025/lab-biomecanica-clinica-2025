import streamlit as st

# Define los nombres de tus páginas
paginas = [
    "Página principal",
    "Bienvenida",
    "Introducción",
    "Unidad 1: Bioinstrumentación",
    "Unidad 1: Control motor",
    "Unidad 2: Balance",
    "Unidad 3: Marcha",
]

# Inicializa el estado si no existe aún
if "indice_pagina" not in st.session_state:
    st.session_state.indice_pagina = 0

# Muestra la página actual
pagina_actual = paginas[st.session_state.indice_pagina]
st.title(pagina_actual)

# Aquí puedes condicionar el contenido por página si quieres
if pagina_actual == "Página principal":
    st.write("Bienvenido a la página principal.")
elif pagina_actual == "Bienvenida":
    st.write("¡Hola! Esta es la bienvenida.")
elif pagina_actual == "Introducción":
    st.write("Contenido de la introducción.")
elif pagina_actual == "Unidad 1: Bioinstrumentación":
    st.write("Contenido de Bioinstrumentación.")
elif pagina_actual == "Unidad 1: Control motor":
    st.write("Contenido de Control Motor.")
elif pagina_actual == "Unidad 2: Balance":
    st.write("Contenido de Balance.")
elif pagina_actual == "Unidad 3: Marcha":
    st.write("Contenido de Análisis de Marcha.")

# Botones de navegación
col1, col2 = st.columns([1, 1])
with col1:
    if st.button("⬅️ Anterior", use_container_width=True):
        if st.session_state.indice_pagina > 0:
            st.session_state.indice_pagina -= 1

with col2:
    if st.button("Siguiente ➡️", use_container_width=True):
        if st.session_state.indice_pagina < len(paginas) - 1:
            st.session_state.indice_pagina += 1
