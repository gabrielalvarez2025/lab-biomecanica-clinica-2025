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
    3. Se usará automáticamente el archivo `.mot` y podrás elegir el video de cualquier cámara.  
    """)

    uploaded_zip = st.file_uploader("📂 Sube el archivo ZIP de OpenCap", type=["zip"])

    if uploaded_zip is not None:
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
                # Obtener .mot
                mot_path = [f for f in mot_files if os.path.basename(f).startswith(selected_trial)][0]

                # Detectar todos los videos disponibles para este trial
                video_cams = sorted([
                    f for f in file_list 
                    if "Videos/" in f and f.endswith((".mp4", ".mov")) and os.path.basename(f).startswith(selected_trial)
                ])

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

                # --- Graficar Ángulo vs Tiempo ---
                st.markdown("### Gráfico Ángulo vs Tiempo")
                y_cols = st.multiselect(
                    "Selecciona una o varias columnas (eje Y):",
                    options=df.columns[1:],
                    default=[],
                    placeholder="Elige una articulación..."
                )

                if y_cols:
                    # Manejo de cámara con botones
                    if "cam_index" not in st.session_state:
                        st.session_state.cam_index = 0

                    col_left, col_center, col_right = st.columns([1, 2, 1])
                    with col_left:
                        if st.button("⬅️"):
                            st.session_state.cam_index = max(0, st.session_state.cam_index - 1)
                    with col_right:
                        if st.button("➡️"):
                            st.session_state.cam_index = min(len(video_cams) - 1, st.session_state.cam_index + 1)

                    if video_cams:
                        current_cam_path = video_cams[st.session_state.cam_index]
                        st.write(f"Mostrando video: {os.path.basename(current_cam_path).split('/')[1]}")  # ej: Cam0, Cam1...
                        with z.open(current_cam_path) as vfile:
                            video_bytes = vfile.read()
                        uploaded_video = io.BytesIO(video_bytes)
                    else:
                        uploaded_video = None

                    # Columnas para video y gráfico
                    if uploaded_video is not None:
                        col_plot1, col_plot2 = st.columns([1, 3])
                    else:
                        col_plot2, = st.columns(1)

                    if uploaded_video is not None:
                        with col_plot1:
                            st.video(uploaded_video, loop=True, muted=True)

                    with col_plot2:
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
                                x=0.79,
                                y=1.3,
                                bgcolor="rgba(255,255,255,0.2)",
                                bordercolor="black",
                                borderwidth=1
                            )
                        )
                        st.plotly_chart(fig, use_container_width=True)

                # --- Graficar Ángulo-Ángulo ---
                st.markdown("---")
                st.markdown("### Gráfico Ángulo-Ángulo")
                col_angle_1, col_angle_2 = st.columns(2)
                with col_angle_1:
                    eje_x = st.selectbox(
                        "Selecciona la columna para el eje X:",
                        options=df.columns[1:],
                        placeholder="Selecciona una articulación para el Eje X..."
                    )
                with col_angle_2:
                    eje_y = st.selectbox(
                        "Selecciona la columna para el eje Y:",
                        options=df.columns[1:],
                        placeholder="Selecciona una articulación para el Eje Y..."
                    )

                if eje_x and eje_y:
                    if uploaded_video is not None:
                        col_plot_ang_1, col_plot_ang_2 = st.columns([1, 3])
                    else:
                        col_plot_ang_2, = st.columns(1)

                    if uploaded_video is not None:
                        with col_plot_ang_1:
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
                            title=f"Gráfico Ángulo–Ángulo ({eje_y} vs {eje_x})",
                            xaxis_title=eje_x,
                            yaxis_title=eje_y,
                            template="plotly_white",
                            yaxis=dict(scaleanchor="x", scaleratio=1)
                        )
                        st.plotly_chart(fig, use_container_width=True)
