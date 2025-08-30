import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go
import os
import zipfile


def main_opencap():
    
    col_zip_1, col_zip_2 = st.columns(2)

    with col_zip_1:
        st.markdown("### Sube una carpeta ZIP:")
        st.markdown("""
        1. Sube el **.zip** exportado de OpenCap.  
        2. Selecciona el **trial** que quieres analizar.  
        3. Se usará automáticamente el archivo **.mot** correspondiente al trial.  
        """)
    with col_zip_2:
        st.markdown(" ")
        
        uploaded_zip = st.file_uploader("📂 Sube el archivo ZIP de OpenCap", type=["zip"])

    if uploaded_zip is not None:
        # Extraer lista de archivos dentro del ZIP
        with zipfile.ZipFile(uploaded_zip, "r") as z:
            file_list = z.namelist()

            # Buscar los .mot dentro de OpenSimData/Kinematics/ (excepto artefactos de re-comprimir en Mac, que comienzan con "._")
            mot_files = [
                f for f in file_list
                if "OpenSimData/Kinematics/" in f
                and f.endswith(".mot")
                and not os.path.basename(f).startswith("._")  # ❌ ignorar artefactos
            ]

            if not mot_files:
                st.error("⚠️ No se encontraron archivos .mot en la carpeta ZIP")
                return

            # Lista de trials (sin ruta, solo nombre)
            trials = [os.path.splitext(os.path.basename(f))[0] for f in mot_files]

            
            
            # --- Seleccionar Trial --- #
            
            st.markdown("---")
            
            col_trial_1, col_trial_2 = st.columns(2)

            with col_trial_1:
                st.markdown("### Elige un Trial:")

            with col_trial_2:
                # Selección de trial
                selected_trial = st.selectbox("Selecciona el trial:", trials, index=None, placeholder=None)
                if selected_trial:
                    # --- Mostrar nombre de trial ---
                    st.success(f"✅ Trial seleccionado: **{selected_trial}**")
                    st.markdown("Puedes cambiarlo cuando desees.")
            
            st.markdown("---")

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
                cam_map = {int(cam[-1])+1: cam for cam in cams_disponibles}

                


                def render_video(z, video_paths, cam_map, label="label"):
                    # Renderiza un segmented control que actualiza st.session_state
                    key_name = f"cam_key_{label}"  # clave única para Streamlit
                    if 'cam_key' not in st.session_state:
                        st.session_state.cam_key = list(cam_map.keys())[0]

                    

                    cam_selected = st.segmented_control(
                        "Elige una cámara:",
                        list(cam_map.keys()),
                        default=st.session_state.cam_key,
                        key=key_name,
                        width="stretch"
                    )
                    
                    # Actualizar el session_state
                    st.session_state.cam_key = cam_selected
                    selected_cam = cam_map[st.session_state.cam_key]

                    # Cargar el video correspondiente
                    selected_video_paths = [p for p in video_paths if get_cam_name(p) == selected_cam]
                    uploaded_video = None
                    if selected_video_paths:
                        with z.open(selected_video_paths[0]) as vfile:
                            video_bytes = vfile.read()
                        uploaded_video = io.BytesIO(video_bytes)
                    
                    st.video(uploaded_video, loop=True, muted=True, autoplay=True)
                    
                    return uploaded_video





                
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

                

                

                # --- Mostrar DataFrame ---
                st.markdown("### Vista previa de los datos")

                st.markdown("La grabación que realizaste con OpenCap es un tipo de **videofotogramtería** (VFG). ")
                
                
                col_text_tabla_1, col_text_tabla_2 = st.columns(2)

                with col_text_tabla_1:

                    st.markdown("""
                        Esto quiere decir que capturaste datos de imagen (videos) mediante una cámara y que utilizaste esos videos para calcular métricas cinemáticas.
                        
                        En una VFG clásica, utilizarías herramientas digitales para tomar estas medidas a mano a partir de tu imagen: medir ángulos, distancias, calcular tiempos, estimar velocidades, etc.
                                """)
                
                with col_text_tabla_2:
                    st.markdown("""
                        Uno de los beneficios de OpenCap es que automatiza el calculo de estas métricas a partir de los videos; ya no debes calcularlas de forma manual, sino que el sistema te las entrega directamente ya calculadas.
                                
                        OpenCap calcula específicamente datos de **ángulos articulares** en el tiempo.
                                """)
                    
                st.markdown("A continuación, podrás ver los datos de ángulo articular (en grados) que OpenCap calculó para varias articulaciones. La primera columna muestra el instante de tiempo (en segundos) en que se obtuvo ese ángulo articular.")



                st.dataframe(df, hide_index=True)

                # --- Descargar Excel ---
                esp_boton_1, col_boton, esp_boton_2 = st.columns(3)
                
                with col_boton:
                    towrite = io.BytesIO()
                    df.to_excel(towrite, index=False, engine="openpyxl")
                    towrite.seek(0)
                    
                    st.download_button(
                        label="📥 Descargar como Excel",
                        data=towrite,
                        file_name=f"{selected_trial}.xlsx",
                        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                        use_container_width=True
                    )

                
                # --- Graficar ---

                st.markdown("---")

                # Selección de columnas para graficar en el tiempo

                col_plot_time_1, col_plot_time_2 = st.columns(2)

                with col_plot_time_1:
                    st.markdown("### Gráfico Ángulo vs Tiempo")
                
                with col_plot_time_2:
                    st.markdown(" ")
                    y_cols = st.multiselect(
                        "Selecciona una o varias columnas (eje Y):",
                        options=df.columns[1:],
                        default=[],
                        placeholder="Elige una articulación..."
                    )

                if y_cols:

                    if video_paths:
                        col_plot1, col_plot2 = st.columns([1, 3])

                        with col_plot1:
                            st.markdown(" ")
                            uploaded_video = render_video(z, video_paths, cam_map, label="Ángulo vs Tiempo")

                    else:
                        col_plot2, = st.columns(1)
                    
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
                            title=f"Movimiento angular en el tiempo para {selected_trial}",
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
                st.markdown("### Gráfico Ángulo-Ángulo (ciclograma)")

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

                    if video_paths:
                        col_plot_ang_1, col_plot_ang_2 = st.columns([1, 3])

                        with col_plot_ang_1:
                            uploaded_video
                    else:
                        col_plot_ang_2, = st.columns(1)

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
                
                
                # Comparando gráficos entre trials
                st.markdown("---")
                st.markdown("### Comparemos varios trials")
                st.markdown(f"Ahora que revisaste cómo se comportan los datos de las articulaciones durante el trial que seleccionaste ({selected_trial}), puedes usar el selector de abajo para seleccionar múltiples trials y comparar cómo se comporta cada articulación entre diferentes trials.")

                col_select_trial_1, col_select_trial_2 = st.columns(2)

                with col_select_trial_1:
                    selected_trials = st.multiselect(
                        "Selecciona uno o varios trials para comparar:",
                        options=trials,
                        default=[selected_trial]  # por defecto el trial actual
                    )

                with col_select_trial_2:
                    selected_joint = st.selectbox(
                        "Selecciona una articulación:",
                        options=df.columns[1:],  # todas menos "time"
                        index=None,
                        placeholder="Elige una articulación..."
                    )

                if selected_trials and selected_joint:
                    fig_compare = go.Figure()

                    for trial in selected_trials:
                        # Buscar .mot del trial
                        mot_path_trial = [f for f in mot_files if os.path.basename(f).startswith(trial)][0]

                        with z.open(mot_path_trial) as mot_file_trial:
                            file_content_trial = mot_file_trial.read().decode("utf-8").splitlines()

                        # Cortar header
                        header_lines_trial = 0
                        for i, line in enumerate(file_content_trial):
                            if "endheader" in line:
                                header_lines_trial = i + 1
                                break

                        data_str_trial = "\n".join(file_content_trial[header_lines_trial:])
                        data_buffer_trial = io.StringIO(data_str_trial)

                        df_trial = pd.read_csv(data_buffer_trial, delimiter=r"\s+", engine="python")

                        # Agregar curva al gráfico
                        fig_compare.add_trace(go.Scatter(
                            x=df_trial[df_trial.columns[0]],  # tiempo
                            y=df_trial[selected_joint],
                            mode="lines",
                            name=trial
                        ))

                    fig_compare.update_layout(
                        title=f"Comparación de {selected_joint} entre Trials",
                        xaxis_title="Tiempo (s)",
                        yaxis_title="Ángulo (°)",
                        template="plotly_white",
                        legend=dict(
                            x=0.8,
                            y=1.1,
                            bgcolor="rgba(255,255,255,0.3)",
                            bordercolor="black",
                            borderwidth=1
                        )
                    )

                    st.plotly_chart(fig_compare, use_container_width=True)
