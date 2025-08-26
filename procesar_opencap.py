import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go
import os

def main_opencap():
    st.subheader("📊 Procesar archivo OpenCap (.mot)")

    st.markdown("""
    1. Busca la carpeta **📂 Kinematics**.
    2. Sube el archivo **.mot** correspondiente al Trial que te interesa convertir/visualizar/analizar.
    """)

    col_init1, col_init2 = st.columns(2)

    with col_init1:
        uploaded_file = st.file_uploader("📂 Sube un archivo .mot exportado de OpenCap", type=["mot"])
    with col_init2:
        uploaded_video = st.file_uploader("📹 (Opcional) Sube un *video* del gesto", 
                                          type=["mp4", "mov", "avi", "mkv"])

    if uploaded_file is not None:

        base_filename = os.path.splitext(uploaded_file.name)[0]

        file_content = uploaded_file.getvalue().decode("utf-8").splitlines()

        # Buscar línea endheader
        header_lines = 0
        for i, line in enumerate(file_content):
            if "endheader" in line:
                header_lines = i + 1
                break

        data_str = "\n".join(file_content[header_lines:])
        data_buffer = io.StringIO(data_str)
        df = pd.read_csv(data_buffer, delimiter=r"\s+", engine="python")

        col1, col2 = st.columns(2)
        with col1:
            st.success(f"✅ Archivo '{uploaded_file.name}' cargado")
        with col2:
            towrite = io.BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)
            st.download_button(
                label="📥 Descargar Excel",
                data=towrite,
                file_name=f"{base_filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        st.markdown("### Vista previa del DataFrame")
        st.dataframe(df, hide_index=True)

        # 🔹 Sincronización manual con slider
        st.markdown("### Control de Tiempo (Video + Gráfico)")
        tiempo_sel = st.slider(
            "Selecciona el tiempo (s)",
            min_value=float(df[df.columns[0]].min()),
            max_value=float(df[df.columns[0]].max()),
            value=float(df[df.columns[0]].min()),
            step=0.01
        )

        # --- Mostrar video ---
        if uploaded_video is not None:
            st.video(uploaded_video, start_time=int(tiempo_sel))  # inicia el video en el tiempo elegido

        # Selección de columnas Y
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

            # Línea vertical en el tiempo seleccionado
            fig.add_vline(x=tiempo_sel, line_width=2, line_dash="dash", line_color="red")

            fig.update_layout(
                title="Curvas seleccionadas",
                xaxis_title="Tiempo (s)",
                yaxis_title="Ángulo (°)",
                template="plotly_white"
            )
            st.plotly_chart(fig, use_container_width=True)
