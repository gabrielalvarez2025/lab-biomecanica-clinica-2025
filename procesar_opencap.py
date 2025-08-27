import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go
import os

def main_opencap():
    st.subheader("Procesar archivos OpenCap desde carpeta")

    st.markdown("""
    1. Sube todos los archivos de la carpeta OpenCap descomprimida.  
    2. Selecciona el trial que quieres analizar.  
    """)

    uploaded_files = st.file_uploader(
        "📂 Sube los archivos de la carpeta descomprimida",
        accept_multiple_files=True
    )

    if uploaded_files:
        # Filtrar solo archivos .mot
        mot_files = [f for f in uploaded_files if "OpenSimData/Kinematics/" in f.name and f.name.endswith(".mot")]

        if not mot_files:
            st.error("⚠️ No se encontraron archivos .mot en la carpeta subida")
            return

        # Lista de trials
        trials = [os.path.splitext(os.path.basename(f.name))[0] for f in mot_files]

        selected_trial = st.selectbox("Selecciona el trial:", trials)

        if selected_trial:
            # Obtener el archivo .mot correspondiente
            mot_file = [f for f in mot_files if os.path.basename(f.name).startswith(selected_trial)][0]

            # Leer el archivo .mot
            file_content = mot_file.getvalue().decode("utf-8").splitlines()

            # Cortar hasta endheader
            header_lines = 0
            for i, line in enumerate(file_content):
                if "endheader" in line:
                    header_lines = i + 1
                    break
            data_str = "\n".join(file_content[header_lines:])
            data_buffer = io.StringIO(data_str)

            df = pd.read_csv(data_buffer, delimiter=r"\s+", engine="python")

            st.success(f"✅ Trial seleccionado: {selected_trial}")

            # Descargar Excel
            towrite = io.BytesIO()
            df.to_excel(towrite, index=False, engine="openpyxl")
            towrite.seek(0)
            st.download_button(
                label="📥 Descargar Excel",
                data=towrite,
                file_name=f"{selected_trial}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # Mostrar DataFrame
            st.markdown("### Vista previa del DataFrame")
            st.dataframe(df, hide_index=True)

            # Buscar video Cam0 para ese trial
            video_file = None
            for f in uploaded_files:
                if f.name.startswith("Videos/Cam0/") and f.name.endswith((".mp4", ".mov")) and os.path.basename(f.name).startswith(selected_trial):
                    video_file = f
                    break

            if video_file:
                st.video(video_file, loop=True, muted=True)

            # Graficar
            st.markdown("### Gráfico Ángulo vs Tiempo")
            y_cols = st.multiselect(
                "Selecciona una o varias columnas (eje Y):",
                options=df.columns[1:],
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
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)
