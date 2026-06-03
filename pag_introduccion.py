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

    # --- NUEVO DISEÑO CSS AJUSTADO Y CORREGIDO ---
    st.markdown(
        """
        <style>
        .wrapper-carrusel {
            width: 100%;
            overflow: hidden;
        }
        .carrusel-container {
            display: flex;
            overflow-x: auto;
            scroll-snap-type: x mandatory;
            scroll-behavior: smooth;
            gap: 30px;
            padding: 15px;
            width: 100%;
            box-sizing: border-box;
        }
        /* Forzar que aparezca la barra si es necesario o esconderla limpiamente */
        .carrusel-container::-webkit-scrollbar {
            height: 6px;
        }
        .carrusel-container::-webkit-scrollbar-thumb {
            background-color: #333;
            border-radius: 10px;
        }
        
        /* Aseguramos dimensiones fijas absolutas para que no se colapse la estructura */
        .tarjeta-story-doble {
            flex: 0 0 650px; /* Impide que la tarjeta se encoja o colapse */
            width: 650px;
            height: 400px;
            background-color: #1a1a1a;
            border-radius: 14px;
            border: 2px solid #2d2d2d;
            scroll-snap-align: center;
            display: flex !important; /* Forzar comportamiento horizontal */
            flex-direction: row !important;
            overflow: hidden;
            box-shadow: 0 8px 20px rgba(0,0,0,0.6);
        }
        
        /* Columna Izquierda: Video */
        .col-video {
            width: 50% !important;
            height: 100% !important;
            background-color: #000000;
            display: flex;
            align-items: center;
            justify-content: center;
            overflow: hidden;
        }
        
        /* Ajuste del reproductor de video para que no se corte */
        .col-video video {
            width: 100% !important;
            height: 100% !important;
            object-fit: contain !important; /* Muestra el video completo sin recortes */
        }
        
        /* Columna Derecha: Texto */
        .col-texto {
            width: 50% !important;
            height: 100% !important;
            padding: 20px;
            box-sizing: border-box;
            background-color: #121212;
            display: flex;
            flex-direction: column;
            overflow-y: auto;
        }
        
        .titulo-docente {
            font-size: 15px;
            font-weight: bold;
            color: #FF4B4B;
            margin-bottom: 10px;
            border-bottom: 1px solid #333;
            padding-bottom: 5px;
        }
        
        .cuerpo-docente {
            font-size: 13px;
            line-height: 1.5;
            color: #e0e0e0;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    urls_completas = []
    for item in st.session_state.videos_feed:
        with st.spinner("Cargando portafolio de movimiento..."):
            url_mp4 = obtener_url_video_directo(item["url"])
            if url_mp4:
                urls_completas.append(
                    {
                        "mp4": url_mp4,
                        "titulo": item["titulo"],
                        "comentario": item["comentario"],
                    }
                )

    # --- ARMADO DEL HTML ---
    html_carrusel = '<div class="wrapper-carrusel"><div class="carrusel-container">'

    for item in urls_completas:
        html_carrusel += f"""
        <div class="tarjeta-story-doble">
            <div class="col-video">
                <video autoplay muted loop playsinline controls>
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

    html_carrusel += "</div></div>"

    # CLAVE: Forzamos el ancho del iframe a true completo usando use_container_width
    st.components.v1.html(html_carrusel, height=450, scrolling=False)

    if st.button("🎲 Mezclar Casos Clínicos", use_container_width=True):
        st.session_state.videos_feed = random.sample(
            DATABASE_VIDEOS, len(DATABASE_VIDEOS)
        )
        st.rerun()

