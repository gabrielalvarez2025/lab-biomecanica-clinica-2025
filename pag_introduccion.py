import streamlit as st
import random
import yt_dlp

def obtener_url_video_directo(url_instagram):
    """
    Usa yt-dlp para extraer la URL real del archivo .mp4
    evitando los bloqueos de iframe de Instagram.
    """
    ydl_opts = {
        'format': 'best',
        'quiet': True,
        'no_warnings': True,
    }
    try:
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(url_instagram, download=False)
            # Retorna el enlace directo al .mp4 que expira en unas horas,
            # pero como se ejecuta en tiempo real para el alumno, siempre estará activo.
            return info.get('url', None)
    except Exception:
        return None

def main_introduccion():
    st.header("Introducción al análisis del movimiento")
    st.markdown("---")
    st.subheader("📱 Biomecánica Reels: *Doomscrolling* para Ñoños v3")

    LISTA_VIDEOS = [
        "https://www.instagram.com/p/DXSdAOnimiF/",
        "https://www.instagram.com/p/DYF_XhqTTby/",
        "https://www.instagram.com/p/DY9ahGasLK1/",
    ]

    if "videos_feed" not in st.session_state:
        st.session_state.videos_feed = random.sample(LISTA_VIDEOS, len(LISTA_VIDEOS))

    if st.button("🔄 Generar nuevo feed aleatorio"):
        st.session_state.videos_feed = random.sample(LISTA_VIDEOS, len(LISTA_VIDEOS))
        st.rerun()

    with st.container(height=600, border=True):
        for url in st.session_state.videos_feed:
            st.markdown("**🤖 Análisis de caso en el feed:**")

            if "instagram.com" in url:
                # Mostramos un spinner de carga mientras Python extrae el video en segundo plano
                with st.spinner("Cargando video desde Instagram..."):
                    video_directo_url = obtener_url_video_directo(url)
                
                if video_directo_url:
                    # Cargamos el reproductor nativo con el .mp4 extraído
                    st.video(video_directo_url)
                else:
                    # Respaldo por si falla la extracción
                    st.warning("No se pudo previsualizar el video directamente.")
                    st.page_link(url, label="📸 Ver directamente en Instagram", icon="🔗")
            else:
                st.video(url)

            st.markdown("<hr style='border:1px dashed #7d7d7d'><br>", unsafe_allow_html=True)