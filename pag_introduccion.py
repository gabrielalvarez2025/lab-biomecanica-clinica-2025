import random
import streamlit as st
import yt_dlp


def obtener_url_video_directo(url_instagram):
    ydl_opts = {
        "format": "best",
        "quiet": True,
        "no_warnings": True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url_instagram, download=False)
            return info.get("url", None)
    except Exception:
        return None


def main_introduccion():
    st.header("Introducción al análisis del movimiento")
    st.markdown("---")

    st.subheader("Reels biomecánicos para ñoños")
    st.markdown("Te dejamos acá una selección de algunos videos sacados de Instagram, TikTok, YouTube Shorts y otras plataformas, que podrían resultarte interesantes y complementar contenidos vistos en clase. Cada uno se acompaña de un breve comentario de nuestra parte destacando alguno de los aspectos que podrían ser relevantes para el curso. La idea es que puedas entretenerte con este contenido curado para ti cuando estés aburrido. Estaremos continuamente haciendo crecer la colección de videos.")

    # 1. Base de datos estructurada con tus comentarios docentes o Lorem Ipsum
    DATABASE_VIDEOS = [
        {
            "url": "https://www.instagram.com/p/DXSdAOnimiF/",
            "titulo": "",
            "comentario": "resulta interesante observar el control del tronco durante la vocalización. La acción coordinada de transverso abdominal, multífidos, diafragma y piso pélvico genera un cilindro estable que minimiza movimientos indeseados del tronco y evita una pérdida brusca de presión, permitiendo dosificar la salida de aire de manera eficiente. Esto es especialmente relevante al cantar, ya que la tarea requiere mantener una presión subglótica relativamente constante durante períodos prolongados. La estabilidad proporcionada por el sistema muscular profundo permite desacoplar parcialmente la función postural de la función respiratoria, evitando que las oscilaciones asociadas a la ventilación comprometan la postura o que las exigencias posturales interfieran con la producción vocal. Es un buen ejemplo de cómo los músculos estabilizadores no solo contribuyen a la estabilidad lumbopélvica, sino también al control respiratorio y al desempeño global de la tarea.",
        },
        {
            "url": "https://www.instagram.com/p/DYF_XhqTTby/",
            "titulo": "Caso 2: Dinámica y torque lumbar en levantamiento",
            "comentario": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Analicen detalladamente la coactivación muscular y cómo la transferencia de fuerzas a través de la fascia toracolumbar contribuye a la estabilidad del core.",
        },
        {
            "url": "https://www.instagram.com/p/DY9ahGasLK1/",
            "titulo": " ",
            "comentario": "Recordar: Gran parte del movimiento global de la extremidad inferior durante la marcha y otras actividades, está mediado por la inercia y transferencia de momentum desde movimientos previos y activación de la musculatura proximal. Somos altamente eficientes debido a que gran parte de los movimientos que realizamos aprovechan la física de los cuerpos rígidos que componen nuestros segmentos para ahorrar energía y utilizar sólo la activación muscular estrictamente necesaria para lograr la tarea.",
        },
    ]

    # 2. Inicializar el feed aleatorio en la sesión si no existe
    if "videos_feed" not in st.session_state:
        st.session_state.videos_feed = random.sample(
            DATABASE_VIDEOS, len(DATABASE_VIDEOS)
        )

    # 3. Inicializar el índice del video actual
    if "reels_index" not in st.session_state:
        st.session_state.reels_index = 0

    # Obtener el caso actual basado en el índice
    idx = st.session_state.reels_index
    caso_actual = st.session_state.videos_feed[idx]

    # --- DISEÑO DE DOS COLUMNAS NATIVAS ---
    col_izquierda, col_derecha = st.columns([1.2, 1], gap="large")

    # COLUMNA IZQUIERDA: El Video (Escalado proporcional automático)
    with col_izquierda:
        with st.spinner("Extrayendo flujo multimedia..."):
            video_directo_url = obtener_url_video_directo(caso_actual["url"])

        if video_directo_url:
            # El componente nativo se adapta perfectamente al ancho de la columna sin cortarse
            st.video(video_directo_url)
        else:
            st.error("No se pudo cargar la previsualización del video.")
            st.page_link(caso_actual["url"], label="Ver en Instagram", icon="📸")

    # COLUMNA DERECHA: El Texto Académico Sincronizado
    with col_derecha:
        st.markdown(f"### 🧠 {caso_actual['titulo']}")
        st.markdown(
            f"<p style='text-align: justify; font-size: 14px;'>{caso_actual['comentario']}</p>",
            unsafe_allow_html=True,
        )

        st.write("")  # Espaciador estético

        # --- BOTONES DE NAVEGACIÓN DENTRO DE LA COLUMNA DE TEXTO ---
        st.markdown("**Navegación de casos:**")
        col_btn_prev, col_btn_next = st.columns(2)

        with col_btn_prev:
            # Desactivar botón si estamos en el primer video
            if st.button(
                "⬅️ Anterior",
                use_container_width=True,
                disabled=(idx == 0),
            ):
                st.session_state.reels_index -= 1
                st.rerun()

        with col_btn_next:
            # Desactivar botón si estamos en el último video
            if st.button(
                "Siguiente ➡️",
                use_container_width=True,
                disabled=(idx == len(st.session_state.videos_feed) - 1),
            ):
                st.session_state.reels_index += 1
                st.rerun()

        st.caption(
            f"<center>Caso {idx + 1} de {len(st.session_state.videos_feed)}</center>",
            unsafe_allow_html=True,
        )

    # --- BOTÓN INFERIOR GENERAL PARA BARAJAR ---
    st.markdown("---")
    if st.button("🎲 Mezclar y reiniciar orden de casos", use_container_width=True):
        st.session_state.videos_feed = random.sample(
            DATABASE_VIDEOS, len(DATABASE_VIDEOS)
        )
        st.session_state.reels_index = 0
        st.rerun()

