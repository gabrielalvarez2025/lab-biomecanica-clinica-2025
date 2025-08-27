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
                video_candidates = [
                    f for f in file_list 
                    if f"Videos/Cam0" in f and f.endswith((".mp4", ".mov")) and os.path.basename(f).startswith(selected_trial)
                ]

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

                # --- Mostrar video (si existe) ---
                uploaded_video = None
                if video_candidates:
                    video_path = video_candidates[0]
                    with z.open(video_path) as vfile:
                        video_bytes = vfile.read()
                    uploaded_video = io.BytesIO(video_bytes)
                    st.video(uploaded_video, loop=True, muted=True)

                # --- Graficar ---
                st.markdown("### Gráfico Ángulo vs Tiempo")
                y_cols = st.multiselect(
                    "Selecciona una o varias columnas (eje Y):",
                    options=df.columns[1:],
                    default=[],
                    placeholder="Elige una articulación..."
                )

                if y_cols:
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
