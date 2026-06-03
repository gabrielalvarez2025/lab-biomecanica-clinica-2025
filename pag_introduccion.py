import random
import streamlit as st


def main_introduccion():
    st.header("Introducción al análisis del movimiento")

    # --- NUEVA SECCIÓN: DOOMSCROLLING ACADÉMICO ---
    st.markdown("---")
    st.subheader("📱 Biomecánica Reels: *Doomscrolling* para Ñoños")
    st.write(
        "¿Perdiendo el tiempo? Mejor aprovéchalo analizando movimiento. "
        "Desliza hacia abajo para ver contenido aleatorio de redes sociales sobre biomecánica."
    )

    # 1. Base de datos de links (Reels, Shorts, TikToks o Videos directos)
    # Nota: Los links de Instagram se renderizan mejor en Streamlit usando su formato de "embed"
    LISTA_VIDEOS = [
        "https://www.instagram.com/p/DXSdAOnimiF/",
        "https://www.instagram.com/p/DYF_XhqTTby/",
        "https://www.instagram.com/p/DY9ahGasLK1/",
        # Puedes agregar aquí YouTube Shorts (cambiando 'shorts/' por 'watch?v=' funciona nativamente con st.video)
        # "https://www.youtube.com/watch?v=VIDEO_ID"
    ]

    # 2. Inicializar el estado de la sesión para mantener los videos seleccionados
    if "videos_feed" not in st.session_state:
        # Mezclar la lista por primera vez y tomar una selección o dejarla toda al azar
        st.session_state.videos_feed = random.sample(
            LISTA_VIDEOS, len(LISTA_VIDEOS)
        )

    # Botón tipo "Swipe" para recargar/mezclar el feed
    if st.button("🔄 Generar nuevo feed aleatorio"):
        st.session_state.videos_feed = random.sample(
            LISTA_VIDEOS, len(LISTA_VIDEOS)
        )
        st.rerun()

    # 3. Contenedor con scroll vertical simulado
    # Definimos una altura fija para forzar la barra de desplazamiento dentro de la ventana
    with st.container(height=600, border=True):
        for url in st.session_state.videos_feed:
            st.markdown(
                f"**🤖 Análisis de caso en el feed:**"
            )  # Título o separador estético

            if "instagram.com" in url:
                # Formatear el link para el iframe de Instagram Embed
                # Limpiamos el URL por si tiene parámetros extras
                base_url = url.split("/?")[0]
                embed_url = f"{base_url}/embed"

                # Usamos HTML para centrar e incrustar el Reel con aspecto vertical
                components_html = f"""
                <div style="display: flex; justify-content: center;">
                    <iframe src="{embed_url}" width="360" height="480" frameborder="0" 
                            scrolling="no" allowtransparency="true" allow="encrypted-media">
                    </iframe>
                </div>
                """
                st.components.v1.html(components_html, height=500)

            elif "youtube.com" in url or "youtu.be" in url:
                # El componente nativo de Streamlit maneja muy bien YouTube
                st.video(url)

            else:
                # Opción genérica por si usas videos alojados localmente o en la nube (mp4)
                st.video(url)

            # Separador visual entre un video y otro para dar sensación de feed de App
            st.markdown(
                "<hr style='border:1px dashed #7d7d7d'><br>",
                unsafe_allow_html=True,
            )

    st.caption(
        "Consejo: Usa la barra de desplazamiento del cuadro anterior para hacer scroll infinito por los videos seleccionados."
    )


# Para probar la función localmente si corres este script de forma directa
if __name__ == "__main__":
    main_introduccion()