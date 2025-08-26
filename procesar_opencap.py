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
    
    uploaded_file = st.file_uploader("📂 Sube un archivo .mot exportado de OpenCap", type=["mot"])

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

        col1, col2 = st.columns(2)

        with col1:
            st.success(f"✅ Archivo '{uploaded_file.name}' cargado")
        
        with col2:
            # --- Botón para descargar DataFrame como Excel ---
            towrite = io.BytesIO()
            df.to_excel(towrite, index=False, engine='openpyxl')
            towrite.seek(0)

            st.download_button(
                label="📥 Descargar Excel",
                data=towrite,
                file_name=f"{base_filename}.xlsx",  # mismo nombre del archivo original
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

        # Mostrar preview
        st.markdown("### Vista previa del DataFrame")
        st.dataframe(df, hide_index=True)

        
        # Selección de columnas para graficar
        st.markdown("### Selección de columnas para graficar")
        y_cols = st.multiselect(
            "Selecciona una o varias columnas (eje Y):",
            options=df.columns[1:],  # excluye la primera (tiempo)
            default=[]
        )

        if y_cols:
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
                title="Curvas seleccionadas",
                xaxis_title=df.columns[0],
                yaxis_title="Valor",
                template="plotly_white"
            )

            st.plotly_chart(fig, use_container_width=True)
        

        ####

        # Selección de columnas para graficar ángulo-ángulo
        st.markdown("### Gráfico Ángulo-Ángulo")

        col_angle_1, col_angle_2 = st.columns(2)

        with col_angle_1:
            eje_x = st.selectbox(
                "Selecciona la columna para el eje X:",
                options=df.columns[1:],  # excluye la primera (tiempo)
                placeholder=None,
                index=None
            )

        with col_angle_2:
            eje_y = st.selectbox(
                "Selecciona la columna para el eje Y:",
                options=df.columns[1:],
                index=None,
                placeholder=None
            )

        if eje_x and eje_y:
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