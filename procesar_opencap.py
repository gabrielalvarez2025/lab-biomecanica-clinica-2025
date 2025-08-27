import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go
import os
import zipfile


def main_opencap():
    st.subheader("📦 Procesar carpeta completa de OpenCap (ZIP)")

    st.markdown("""
    1. Sube el **.zip** exportado de OpenCap (toda la carpeta comprimida).  
    2. Selecciona el **trial** que quieres analizar.  
    3. Se usará automáticamente el archivo `.mot` y el video de **Cam0** correspondientes.  
    """)

    uploaded_zip = st.file_uploader("📂 Sube el archivo ZIP de OpenCap", type=["zip"])

    if uploaded_zip is not None:
        # Extraer lista de archivos dentro del ZIP
        with zipfile.ZipFile(uploaded_zip, "r") as z:
            file_list = z.namelist()

            # Buscar los .mot dentro de OpenSimData/Kinematics/
            mot_files = [f for f in file_list if "OpenSimData/Kinematics/" in f and f.endswith(".mot")]

            if not mot_files:
                st.error("⚠️ No se encontraron archivos .mot en la carpeta ZIP")
                return

            # Lista de trials (sin ruta, solo nombre)
            trials = [os.path.splitext(os.path.basename(f))[0] for f in mot_files]

            # Selección de trial
            selected_trial = st.selectbox("Selecciona el trial:", trials)

            if selected_trial:
                # Obtener paths dentro del ZIP
                mot_path = [f for f in mot_files if os.path.basename(f).startswith(selected_trial)][0]
                
                
                # --- Buscar TODAS las rutas de video del trial seleccionado ---
                video_paths = [
                    f for f in file_list
                    if "/Videos/" in f and f.endswith((".mp4", ".mov"))
                    and os.path.basename(f).startswith(selected_trial)  # p.ej. trial.mp4
                ]

                def get_cam_name(p: str):
                    """Devuelve 'Cam0', 'Cam1', ... a partir de una ruta dentro del ZIP."""
                    parts = p.split("/")  # en ZIP siempre '/'
                    try:
                        idx = parts.index("Videos")
                        return parts[idx + 1] if idx + 1 < len(parts) else None
                    except ValueError:
                        return None

                # Lista única de cámaras disponibles
                cams_disponibles = sorted({get_cam_name(p) for p in video_paths if get_cam_name(p)})
                
                # Crear un mapeo: ultimo caracter → nombre completo
                cam_map = {cam[-1]: cam for cam in cams_disponibles}

                # Selectbox para elegir cámara (si hay)
                selected_cam = st.selectbox(
                    "Selecciona la cámara del video:",
                    cams_disponibles
                ) if cams_disponibles else None





                
                # --- Leer .mot ---
                with z.open(mot_path) as mot_file:
                    file_content = mot_file.read().decode("utf-8").splitlines()

                # Cortar hasta endheader
                header_lines = 0
                for i, line in enumerate(file_content):
                    if "endheader" in line:
                        header_lines = i + 1
                        break
                
                data_str = "\n".join(file_content[header_lines:])
                data_buffer = io.StringIO(data_str)

                df = pd.read_csv(data_buffer, delimiter=r"\s+", engine="python")

                # --- Mostrar nombre de trial ---
                st.success(f"✅ Trial seleccionado: {selected_trial}")

                # --- Descargar Excel ---
                esp_boton_1, col_boton, esp_boton_2 = st.columns(3)
                with col_boton:
                    towrite = io.BytesIO()
                    df.to_excel(towrite, index=False, engine="openpyxl")
                    towrite.seek(0)
                    
                    st.download_button(
                        label="📥 Descargar Excel",
                        data=towrite,
                        file_name=f"{selected_trial}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

                # --- Mostrar DataFrame ---
                st.markdown("### Vista previa del DataFrame")
                st.dataframe(df, hide_index=True)

                # Cargar el video correspondiente a la cámara seleccionada
                uploaded_video = None
                if selected_cam:
                    selected_video_paths = [p for p in video_paths if get_cam_name(p) == selected_cam]
                    if selected_video_paths:
                        with z.open(selected_video_paths[0]) as vfile:
                            video_bytes = vfile.read()
                        uploaded_video = io.BytesIO(video_bytes)
                else:
                    st.info("No se encontraron videos para este trial.")
                # --- Graficar ---

                # Selección de columnas para graficar en el tiempo
                st.markdown("### Gráfico Ángulo vs Tiempo")
                y_cols = st.multiselect(
                    "Selecciona una o varias columnas (eje Y):",
                    options=df.columns[1:],
                    default=[],
                    placeholder="Elige una articulación..."
                )

                if y_cols:

                    if uploaded_video is not None:
                        col_plot1, col_plot2 = st.columns([1, 3])
                    else:
                        col_plot2, = st.columns(1)   # 👈 importante: la coma para desempaquetar

                    
                    if uploaded_video is not None:
                        with col_plot1:
                            st.markdown(" ")
                            st.markdown(" ")
                            st.markdown(" ")
                            st.markdown(" ")
                            st.markdown(" ")
                            st.markdown(" ")
                            
                            # --- mover selectbox acá ---
                            selected_cam = st.segmented_control(
                                "Selecciona cámara:",
                                list(cam_map.keys()),
                                default=list(cam_map.keys())[0],
                                width="stretch"
                            )
                            # Recargar video según la cámara elegida
                            # 🔹 Mapear al nombre completo
                            selected_cam = cam_map[selected_cam_short]

                            # Recargar video según la cámara elegida
                            selected_video_paths = [p for p in video_paths if get_cam_name(p) == selected_cam]
                            
                            if selected_video_paths:
                                with z.open(selected_video_paths[0]) as vfile:
                                    video_bytes = vfile.read()
                                uploaded_video = io.BytesIO(video_bytes)


                            st.video(uploaded_video, loop=True, muted=True)

                    
                    with col_plot2:
                        # Crear figura con todas las columnas seleccionadas
                        fig = go.Figure()
                        for col in y_cols:
                            fig.add_trace(go.Scatter(
                                x=df[df.columns[0]],
                                y=df[col],
                                mode="lines",
                                name=col
                            ))

                        fig.update_layout(
                            title="Movimiento angular en el tiempo",
                            xaxis_title="Tiempo (s)",
                            yaxis_title="Ángulo (°)",
                            template="plotly_white",
                            legend=dict(
                                x=0.79, # posición horizontal (0 = izq, 1 = der)
                                y=1.3, # posición vertical (0 = abajo, 1 = arriba)
                                bgcolor="rgba(255,255,255,0.2)", # fondo semi-transparente
                                bordercolor="black",
                                borderwidth=1
                            )
                        )
                        st.plotly_chart(fig, use_container_width=True)
                
                # Selección de columnas para graficar ángulo-ángulo
                st.markdown("---")
                st.markdown("### Gráfico Ángulo-Ángulo")

                col_angle_1, col_angle_2 = st.columns(2)

                with col_angle_1:
                    eje_x = st.selectbox(
                        "Selecciona la columna para el eje X:",
                        options=df.columns[1:],  # excluye la primera (tiempo)
                        placeholder="Selecciona una articulación para el Eje X...",
                        index=None
                    )

                with col_angle_2:
                    eje_y = st.selectbox(
                        "Selecciona la columna para el eje Y:",
                        options=df.columns[1:],
                        index=None,
                        placeholder="Selecciona una articulación para el Eje Y..."
                    )

                
                if eje_x and eje_y:

                    if uploaded_video is not None:
                        col_plot_ang_1, col_plot_ang_2 = st.columns([1, 3])
                    else:
                        col_plot_ang_2, = st.columns(1)   # 👈 importante: la coma para desempaquetar

                    if uploaded_video is not None:
                        with col_plot_ang_1:
                            st.markdown(" ")
                            st.markdown(" ")
                            st.markdown(" ")
                            st.markdown(" ")
                            st.markdown(" ")
                            st.markdown(" ")
                            # flechas cambiar Cam0 - Cam1 - Cam2
                            st.video(uploaded_video, loop=True, muted=True)

                    with col_plot_ang_2:
                    
                        fig = go.Figure()
                        fig.add_trace(go.Scatter(
                            x=df[eje_x],
                            y=df[eje_y],
                            mode='lines',   
                            name=f"{eje_y} vs {eje_x}"
                        ))

                        fig.update_layout(
                            title=f"Gráfico Ángulo–Ángulo   ({eje_y}   vs   {eje_x})",
                            xaxis_title=eje_x,
                            yaxis_title=eje_y,
                            template="plotly_white",
                            yaxis=dict(scaleanchor="x", scaleratio=1)  # 🔹 Mantener proporciones cuadradas
                        )

                        st.plotly_chart(fig, use_container_width=True)
