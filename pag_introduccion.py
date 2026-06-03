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

    st.subheader("📸 Historias de Biomecánica: *Carrusel Académico*")
    st.write(
        "Desliza horizontalmente. A la izquierda verás el gesto motriz y a la derecha nuestra observación docente."
    )

    # 1. Base de datos estructurada: URL + Comentario de los profesores
    DATABASE_VIDEOS = [
        {
            "url": "https://www.instagram.com/p/DXSdAOnimiF/",
            "titulo": "Caso 1: Cinemática de la carrera",
            "comentario": "Observen detalladamente la fase de desaceleración y el ángulo de flexión de la rodilla en el contacto inicial. Analicen cómo influye el torque en la articulación femoropatelar durante el ciclo.",
        },
        {
            "url": "https://www.instagram.com/p/DYF_XhqTTby/",
            "titulo": "Caso 2: Dinámica en levantamiento",
            "comentario": "Pongan atención a la estabilidad de la columna lumbar durante la fase de despegue (first pull). Comparen el comportamiento del centro de masas respecto a los libros de Neumann.",
        },
        {
            "url": "https://www.instagram.com/p/DY9ahGasLK1/",
            "titulo": "Caso 3: Análisis de marcha (OpenCap)",
            "comentario": "Aquí se evidencia la reconstrucción 3D a través de videofotogrametría. Miren la correspondencia entre los vectores de aceleración estimados y los planos anatómicos tradicionales.",
        },
    ]

    if "videos_feed" not in st.session_state:
        st.session_state.videos_feed = random.sample(
            DATABASE_VIDEOS, len(DATABASE_VIDEOS)
        )

    # --- DISEÑO CSS ADAPTADO PARA DOS COLUMNAS ---
    st.markdown(
        """
        <style>
        .carrusel-container {
            display: flex;
            overflow-x: auto;
            scroll-snap-type: x mandatory;
            scroll-behavior: smooth;
            gap: 24px;
            padding: 20px 10px;
            -webkit-overflow-scrolling: touch;
        }
        .carrusel-container::-webkit-scrollbar {
            display: none;
        }
        
        /* Expandimos el ancho de la tarjeta para albergar de forma cómoda las dos columnas */
        .tarjeta-story-doble {
            min-width: 600px;
            max-width: 600px;
            height: 420px;
            background-color: #121212;
            border-radius: 16px;
            border: 2px solid #333;
            scroll-snap-align: center;
            transition: transform 0.3s ease, border-color 0.3s ease;
            display: flex; /* Flexbox horizontal para las dos columnas */
            overflow: hidden;
            box-shadow: 0 4px 15px rgba(0,0,0,0.4);
        }
        
        .tarjeta-story-doble:hover {
            transform: scale(1.02);
            border-color: #FF4B4B;
        }
        
        /* Columna Izquierda: Contenedor del Video */
        .col-video {
            width: 50%;
            height: 100%;
            background-color: #000;
            display: flex;
            align-items: center;
            justify-content: center;
        }
        
        /* Columna Derecha: Contenedor del Texto Académico */
        .col-texto {
            width: 50%;
            height: 100%;
            padding: 24px;
            display: flex;
            flex-direction: column;
            justify-content: flex-start;
            box-sizing: border-box;
            background-color: #1a1a1a;
            color: #ffffff;
            overflow-y: auto; /* Por si el texto del profe es muy largo */
        }
        
        .titulo-docente {
            font-size: 16px;
            font-weight: bold;
            color: #FF4B4B;
            margin-bottom: 12px;
            border-bottom: 1px solid #333;
            padding-bottom: 6px;
        }
        
        .cuerpo-docente {
            font-size: 13.5px;
            line-height: 1.6;
            color: #e0e0e0;
            text-align: justify;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    # Extraer URLs en tiempo real con yt-dlp
    urls_completas = []
    for item in st.session_state.videos_feed:
        with st.spinner("Sincronizando registros biomecánicos..."):
            url_mp4 = obtener_url_video_directo(item["url"])
            if url_mp4:
                urls_completas.append(
                    {
                        "mp4": url_mp4,
                        "titulo": item["titulo"],
                        "comentario": item["comentario"],
                    }
                )

    # --- CONSTRUCCIÓN DEL CONTENEDOR HTML ---
    html_carrusel = '<div class="carrusel-container">'

    for item in urls_completas:
        html_carrusel += f"""
        <div class="tarjeta-story-doble">
            <div class="col-video">
                <video width="100%" height="100%" autoplay muted loop playsinline controls style="object-fit: contain;">
                    <source src="{item['mp4']}" type="video/mp4">
                </video>
            </div>
            
            <div class="col-texto">
                <div class="titulo-docente">🧠 {item['titulo']}</div>
                <div class="cuerpo-docente">
                    <strong>Observación docente:</strong><br>
                    {item['comentario']}
                </div>
            </div>
        </div>
        """

    html_carrusel += "</div>"

    # Inyectamos el componente a la pantalla (ajustamos el height a 480 para dar holgura a las sombras)
    st.components.v1.html(html_carrusel, height=480, scrolling=False)

    if st.button("🎲 Mezclar Casos Clínicos", use_container_width=True):
        st.session_state.videos_feed = random.sample(
            DATABASE_VIDEOS, len(DATABASE_VIDEOS)
        )
        st.rerun()

    st.caption(
        "<center>Desliza horizontalmente para avanzar. Los videos se reproducen de forma automática. Activa el audio interactuando con los controles de cada video.</center>",
        unsafe_allow_html=True,
    )