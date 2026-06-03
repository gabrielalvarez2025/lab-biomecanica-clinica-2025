import random
import streamlit as st
import yt_dlp


@st.cache_data(show_spinner=False)
def precargar_todos_los_videos(lista_casos):
    """Extrae las URLs directas de todos los videos en un solo viaje

    para que la navegación posterior sea instantánea.
    """
    ydl_opts = {
        "format": "best",
        "quiet": True,
        "no_warnings": True,
    }
    resultados = []
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        for caso in lista_casos:
            try:
                info = ydl.extract_info(caso["url"], download=False)
                url_directa = info.get("url", None)
                if url_directa:
                    resultados.append(
                        {
                            "mp4": url_directa,
                            "url_original": caso["url"],
                            "titulo": caso["titulo"],
                            "comentario": caso["comentario"],
                        }
                    )
            except Exception:
                # Si uno falla, avanzamos para no trabar la app
                continue
    return resultados


def main_introduccion():
    st.header("Introducción al análisis del movimiento")
    st.markdown("---")

    st.subheader("Reels biomecánicos para ñoños")
    st.markdown(
        "Te dejamos acá una selección de algunos videos sacados de Instagram, TikTok, YouTube Shorts y otras plataformas... "
        "La idea es que puedas entretenerte con este contenido curado para ti cuando estés aburrido."
    )

    DATABASE_VIDEOS = [
        {
            "url": "https://www.instagram.com/p/DXSdAOnimiF/",
            "titulo": "Caso 1: Control de tronco y presiones",
            "comentario": "Resulta interesante observar el control del tronco durante la vocalización. La acción coordinada de transverso abdominal, multífidos, diafragma y piso pélvico genera un cilindro estable que minimiza movimientos indeseados del tronco y evita una pérdida brusca de presión, permitiendo dosificar la salida de aire de manera eficiente...",
        },
        {
            "url": "https://www.instagram.com/p/DYF_XhqTTby/",
            "titulo": "Caso 2: Dinámica y torque lumbar en levantamiento",
            "comentario": "Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip ex ea commodo consequat. Analicen detalladamente la coactivación muscular y cómo la transferencia de fuerzas a través de la fascia toracolumbar contribuye a la estabilidad del core.",
        },
        {
            "url": "https://www.instagram.com/p/DY9ahGasLK1/",
            "titulo": "Caso 3: Transferencia de momentum",
            "comentario": "Recordar: Gran parte del movimiento global de la extremidad inferior durante la marcha y otras actividades, está mediado por la inercia y transferencia de momentum desde movimientos previos y activación de la musculatura proximal...",
        },
    ]

    # Mezclar la base de datos de manera fija por sesión para que no cambie en cada clic
    if "db_mezclada" not in st.session_state:
        st.session_state.db_mezclada = random.sample(
            DATABASE_VIDEOS, len(DATABASE_VIDEOS)
        )

    # 1. PRECARGA EN UN SOLO BLOQUE (Usa caché para que solo ocurra una vez)
    with st.spinner("Preparando el feed multimedia de forma fluida..."):
        casos_listos = precargar_todos_los_videos(st.session_state.db_mezclada)

    if not casos_listos:
        st.error("No se pudieron conectar los videos en este momento.")
        return

    # Estética para ocultar visualmente las pestañas superiores si se prefiere,
    # pero las dejaremos limpias como un menú de navegación horizontal rápido tipo "Historias"
    st.write("🔽 Selecciona un caso para verlo al instante:")

    # 2. SISTEMA DE TABS (Pestañas) COMO NAVEGADOR INSTANTÁNEO
    nombres_tabs = [f"📹 Video {i+1}" for i in range(len(casos_listos))]
    tabs = st.tabs(nombres_tabs)

    # Renderizar el contenido dentro de cada pestaña
    for idx, tab in enumerate(tabs):
        with tab:
            caso = casos_listos[idx]

            # Estructura de dos columnas nativas idéntica a la anterior
            col_izquierda, col_derecha = st.columns([1.2, 1], gap="large")

            with col_izquierda:
                # El video ya está precargado, arranca de inmediato al cambiar de pestaña
                st.video(caso["mp4"])

            with col_derecha:
                st.markdown(f"### 🧠 {caso['titulo']}")
                st.markdown(
                    f"<p style='text-align: justify; font-size: 14px;'>{caso['comentario']}</p>",
                    unsafe_allow_html=True,
                )

                st.write("")

                # Botón de red social dinámico
                texto_plataforma = "📸 Ver original en Instagram"
                if "tiktok.com" in caso["url_original"]:
                    texto_plataforma = "🎵 Ver original en TikTok"
                elif (
                    "youtube.com" in caso["url_original"]
                    or "youtu.be" in caso["url_original"]
                ):
                    texto_plataforma = "📺 Ver original en YouTube"

                st.link_button(
                    texto_plataforma,
                    caso["url_original"],
                    use_container_width=True,
                )

    # 3. BOTÓN DE REESCRITURA GENERAL (Abajo del todo)
    st.markdown("---")
    if st.button("🎲 Mezclar videos y generar nuevo orden", use_container_width=True):
        st.session_state.db_mezclada = random.sample(
            DATABASE_VIDEOS, len(DATABASE_VIDEOS)
        )
        st.clear_cache()  # Limpia la caché para obligar a buscar nuevas URLs
        st.rerun()