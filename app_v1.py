import streamlit as st

# Define tus páginas con nombres personalizados
pag_principal = "Página principal"
pag_bienvenida = "Bienvenida"
pag_intro = "Introducción"
pag_u1_bio = "Unidad 1: Bioinstrumentación"
pag_u1_motor = "Unidad 1: Control motor"
pag_u2_balance = "Unidad 2: Balance"
pag_u3_marcha = "Unidad 3: Marcha"

# Lista ordenada de páginas
paginas = [pag_principal, pag_bienvenida, pag_intro, pag_u1_bio, pag_u1_motor, pag_u2_balance, pag_u3_marcha]

# Selector de página
pagina_seleccionada = st.radio("Selecciona una página:", paginas)

# Mostrar contenido según página
if pagina_seleccionada == pag_principal:
    st.title(pag_principal)
    st.write("Contenido de la página principal.")

elif pagina_seleccionada == pag_bienvenida:
    st.title(pag_bienvenida)
    st.write("¡Bienvenido/a!")

elif pagina_seleccionada == pag_intro:
    st.title(pag_intro)
    st.write("Contenido introductorio.")

elif pagina_seleccionada == pag_u1_bio:
    st.title(pag_u1_bio)
    st.write("Aquí va el contenido de bioinstrumentación.")

elif pagina_seleccionada == pag_u1_motor:
    st.title(pag_u1_motor)
    st.write("Contenido de control motor.")

elif pagina_seleccionada == pag_u2_balance:
    st.title(pag_u2_balance)
    st.write("Contenido sobre balance.")

elif pagina_seleccionada == pag_u3_marcha:
    st.title(pag_u3_marcha)
    st.write("Análisis de marcha.")
