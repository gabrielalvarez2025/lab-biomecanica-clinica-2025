import streamlit as st
import random

def main_introduccion():
    st.header("Introducción al análisis del movimiento")

    st.markdown("---")
    st.subheader("📱 Biomecánica Reels: *Doomscrolling* para Ñoños x")
    
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
                # Extrae el código del reel para mostrarlo en el texto
                id_reel = url.split("/p/")[1].split("/")[0]
                
                # Diseñamos una tarjeta con aspecto de post
                st.info(f"📸 **Instagram Reel ({id_reel})**")
                st.link_button("▶️ Ver Reel de Biomecánica", url, use_container_width=True)
                st.caption("Haz clic arriba para abrir el video directamente en Instagram.")

            else:
                st.video(url)

            st.markdown("<hr style='border:1px dashed #7d7d7d'><br>", unsafe_allow_html=True)