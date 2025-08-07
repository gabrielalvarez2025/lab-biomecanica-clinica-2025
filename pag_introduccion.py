import streamlit as st
import openai
import random




def mostrar():
    
    
    st.header("Introducción al análisis del movimiento")
    

    # Configura tu clave de API
    openai.api_key = st.secrets["OPENAI_API_KEY"]  # O puedes usar openai.api_key = "tu_clave"

    # Función para pedir una pregunta
    def generar_pregunta():
        prompt = """
    Genera una pregunta de opción múltiple simple sobre biomecánica.

    Formato:
    Pregunta: [una oración donde se describa una situación simple y se le pregunte al estudiante si una variable es cinética o cinemática]
    Opciones:
    A. [opción]
    B. [opción]
    C. [opción]
    D. [opción]
    E. [opción]
    Respuesta correcta: [Letra]
    Explicación: [una breve explicación de por qué la respuesta es correcta]

    La pregunta debe involucrar a una persona (como Juan o María) y una medición usando instrumentos como acelerómetros, dinamómetros, etc.
    Solo debe haber una opción correcta.
    """
        respuesta = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "Eres un profesor de biomecánica."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.7,
        )
        return respuesta['choices'][0]['message']['content']

    # --- UI ---
    st.title("Preguntas interactivas de biomecánica")

    # Almacena pregunta y respuesta en session_state
    if 'pregunta' not in st.session_state:
        st.session_state.pregunta = None
    if 'respuesta_correcta' not in st.session_state:
        st.session_state.respuesta_correcta = None
    if 'explicacion' not in st.session_state:
        st.session_state.explicacion = None

    # Botón para generar nueva pregunta
    if st.button("Generar nueva pregunta"):
        contenido = generar_pregunta()
        partes = contenido.split("Opciones:")
        pregunta = partes[0].replace("Pregunta:", "").strip()
        opciones_raw = partes[1].split("Respuesta correcta:")
        opciones = opciones_raw[0].strip().split("\n")
        respuesta_correcta = opciones_raw[1].split("Explicación:")[0].strip()
        explicacion = opciones_raw[1].split("Explicación:")[1].strip()

        st.session_state.pregunta = pregunta
        st.session_state.opciones = opciones
        st.session_state.respuesta_correcta = respuesta_correcta
        st.session_state.explicacion = explicacion
        st.session_state.seleccion = None

    # Mostrar pregunta actual
    if st.session_state.pregunta:
        st.subheader(st.session_state.pregunta)
        seleccion = st.radio("Selecciona una opción:", st.session_state.opciones, key="opciones_radio")

        if st.button("Enviar respuesta"):
            letra_seleccionada = seleccion.split(".")[0]
            if letra_seleccionada == st.session_state.respuesta_correcta:
                st.success("¡Correcto!")
            else:
                st.error("Incorrecto.")
            st.info(f"Explicación: {st.session_state.explicacion}")