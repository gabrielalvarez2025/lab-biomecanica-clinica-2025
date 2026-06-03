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

    st.subheader("📱 Biomecánica Reels: *Doomscrolling* para Ñoños")

    LISTA_VIDEOS = [
        "https://www.instagram.com/p/DXSdAOnimiF/",
        "https://www.instagram.com/p/DYF_XhqTTby/",
        "https://www.instagram.com/p/DY9ahGasLK1/",
    ]

    # 1. Inicializar el feed aleatorio si no existe
    if "videos_feed" not in st.session_state:
        st.session_state.videos_feed = random.sample(
            LISTA_VIDEOS, len(LISTA_VIDEOS)
        )

    # 2. Inicializar el índice del video actual (en cuál video va el alumno)
    if "reels_index" not in st.session_state:
        st.session_state.reels_index = 0

    # Contenedor estético que simula la pantalla de un teléfono celular
    # Usamos CSS para darle un fondo oscuro, bordes redondeados y centrarlo
    st.markdown(
        """
        <style>
        .phone-frame {
            background-color: #121212;
            border: 4px solid #333333;
            border-radius: 24px;
            padding: 20px;
            margin: 0 auto;
            max-width: 450px;
            box-shadow: 0 10px 25px rgba(0,0,0,0.5);
        }
        .video-header {
            color: #FFFFFF;
            text-align: center;
            font-size: 14px;
            font-weight: bold;
            margin-bottom: 15px;
            letter-spacing: 1px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Renderizamos la "pantalla del teléfono"
    st.markdown('<div class="phone-frame">', unsafe_allow_html=True)

    # Obtener el video correspondiente al índice actual
    idx = st.session_state.reels_index
    url_actual = st.session_state.videos_feed[idx]

    # Encabezado estilo app móvil
    st.markdown(
        f'<div class="video-header">🔥 REEL EN REPRODUCCIÓN ({idx + 1}/{len(st.session_state.videos_feed)})</div>',
        unsafe_allow_html=True,
    )

    # Extraer y mostrar el video actual
    with st.spinner("Conectando con el servidor de contenido..."):
        video_directo_url = obtener_url_video_directo(url_actual)

    if video_directo_url:
        # El reproductor se adapta al ancho de nuestro "teléfono ficticio"
        st.video(video_directo_url)
    else:
        st.error("No se pudo cargar la previsualización de este video.")
        st.page_link(url_actual, label="Abrir en Instagram", icon="📸")

    # Espacio estético
    st.markdown("<br>", unsafe_allow_html=True)

    # --- CONTROLES DE INTERFAZ (Estilo controles verticales de red social) ---
    col_prev, col_rand, col_next = st.columns([1, 2, 1])

    with col_prev:
        # Botón para subir (Video Anterior)
        if st.button("⬆️", use_container_width=True):
            if st.session_state.reels_index > 0:
                st.session_state.reels_index -= 1
                st.rerun()

    with col_rand:
        # Mezclar de nuevo todo el mazo de videos
        if st.button("🎲 Mezclar Todo", use_container_width=True):
            st.session_state.videos_feed = random.sample(
                LISTA_VIDEOS, len(LISTA_VIDEOS)
            )
            st.session_state.reels_index = 0
            st.rerun()

    with col_next:
        # Botón para bajar (Siguiente Video)
        if st.button("⬇️", use_container_width=True):
            if st.session_state.reels_index < len(st.session_state.videos_feed) - 1:
                st.session_state.reels_index += 1
                st.rerun()

    # Cerramos el contenedor HTML del teléfono
    st.markdown("</div>", unsafe_allow_html=True)

    # Pie de página instructivo
    st.caption(
        "<center>Usa las flechas ⬆️ y ⬇️ para navegar de forma estabilizada entre videos como en TikTok.</center>",
        unsafe_allow_html=True,
    )