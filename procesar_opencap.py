import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go
import os
import zipfile


def main_opencap():
    st.subheader("📊 Procesar archivo OpenCap (.mot)")

    st.markdown("""
        1. Busca la carpeta: **📂 OpenSimData > 📂 Kinematics**.
        2. Sube el archivo **📄 .mot** correspondiente al Trial que te interesa convertir/visualizar/analizar.
                    
        """)

    col_init1, col_init2 = st.columns(2)

    with col_init1:
        uploaded_file = st.file_uploader("📂 Sube un archivo .mot exportado de OpenCap", type=["mot"])
    with col_init2:
        # --- Nueva sección: subir video ---
        uploaded_video = st.file_uploader("📹 Si deseas, puedes incluir un *video* del gesto (Opcional)", type=["mp4", "mov", "avi", "mkv"])

    col1, col2 = st.columns(2)

    if uploaded_file is not None:
            with col1:
                st.success(f"✅ Archivo '{uploaded_file.name}' cargado")
        
    if uploaded_video is not None:
        with col2:
            st.success(f"✅ Video '{uploaded_video.name}' cargado")
    
    
    if uploaded_file is not None:
        
        # Guardar el nombre base del archivo (sin extensión) para Excel
        base_filename = os.path.splitext(uploaded_file.name)[0]
        
        # Leer todo el archivo como texto
        file_content = uploaded_file.getvalue().decode("utf-8").splitlines()

        # Buscar la línea con "endheader"
        header_lines = 0
        for i, line in enumerate(file_content):
            if "endheader" in line:
                header_lines = i + 1
                break

        # Cortar todo hasta después de endheader
        data_str = "\n".join(file_content[header_lines:])
        data_buffer = io.StringIO(data_str)

        # Leer el contenido como dataframe separado por espacios
        df = pd.read_csv(data_buffer, delimiter=r"\s+", engine="python")

        

        
            
        
        esp_boton_1, col_boton, esp_boton_2 = st.columns(3)

        with col_boton:
            # --- Botón para descargar DataFrame como Excel ---
            towrite = io.BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)

            st.download_button(
                label="⬇️ Descargar Excel",
                data=towrite,
                file_name=f"{base_filename}.xlsx",  # mismo nombre del archivo original
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
                use_container_width=True
            )

        # Mostrar preview
        st.markdown("### Vista previa del DataFrame")
        st.dataframe(df, hide_index=True)

        
        

        # Selección de columnas para graficar
        st.markdown("### Gráfico Ángulo vs Tiempo")
        y_cols = st.multiselect(
            "Selecciona una o varias columnas (eje Y):",
            options=df.columns[1:],  # excluye la primera (tiempo)
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
                    st.video(uploaded_video)
            
            with col_plot2:
                # Crear figura con todas las columnas seleccionadas
                fig = go.Figure()
                for col in y_cols:
                    fig.add_trace(go.Scatter(
                        x=df[df.columns[0]],
                        y=df[col],
                        mode='lines',
                        name=col
                    ))

                fig.update_layout(
                    title="Movimiento angular en el tiempo",
                    xaxis_title="Tiempo (s)",
                    yaxis_title="Ángulo (°)",
                    template="plotly_white",
                    legend=dict(
                        x=0.79,   # posición horizontal (0 = izq, 1 = der)
                        y=1.3,   # posición vertical (0 = abajo, 1 = arriba)
                        bgcolor="rgba(255,255,255,0.2)",  # fondo semi-transparente
                        bordercolor="black",
                        borderwidth=1
                    )
                )

                st.plotly_chart(fig, use_container_width=True)

        

        
        ####

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
                    st.video(uploaded_video)

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
                    yaxis=dict(scaleanchor="x", scaleratio=1)  # 🔹 Mantener proporciones cuadradas
                )

                st.plotly_chart(fig, use_container_width=True)
    
    