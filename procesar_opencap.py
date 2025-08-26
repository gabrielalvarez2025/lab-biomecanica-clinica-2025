import streamlit as st
import pandas as pd
import io
import os
import zipfile
import plotly.graph_objects as go

def main_opencap():
    st.subheader("📊 Procesar carpeta OpenCap (ZIP)")

    st.markdown("""
    1. Comprime la carpeta del Trial completo en un archivo **.zip**.  
    2. Sube ese ZIP aquí.  
    3. El sistema extraerá automáticamente:  
       - `OpenSimData/Kinematics/sentarse.mot`  
       - `Videos/InputMedia/sentarse/sentarse.mov`
    """)

    uploaded_zip = st.file_uploader("📂 Sube el archivo .zip del Trial", type=["zip"])

    if uploaded_zip is not None:
        st.success(f"✅ Archivo '{uploaded_zip.name}' cargado")

        # --- Extraer archivos dentro del zip ---
        with zipfile.ZipFile(uploaded_zip, "r") as zip_ref:
            file_list = zip_ref.namelist()

            # Buscar los archivos que necesitamos
            mot_path = [f for f in file_list if f.endswith("OpenSimData/Kinematics/sentarse.mot")]
            mov_path = [f for f in file_list if f.endswith("Videos/InputMedia/sentarse/sentarse.mov")]

            if not mot_path:
                st.error("❌ No se encontró el archivo 'sentarse.mot' en la ruta esperada.")
                return
            if not mov_path:
                st.warning("⚠️ No se encontró el archivo 'sentarse.mov'. Se continuará sin el video.")

            # --- Procesar el archivo .mot ---
            mot_file = zip_ref.open(mot_path[0])
            file_content = mot_file.read().decode("utf-8").splitlines()

            # Buscar línea con "endheader"
            header_lines = 0
            for i, line in enumerate(file_content):
                if "endheader" in line:
                    header_lines = i + 1
                    break

            data_str = "\n".join(file_content[header_lines:])
            data_buffer = io.StringIO(data_str)

            # Cargar a DataFrame
            df = pd.read_csv(data_buffer, delimiter=r"\s+", engine="python")

            # Guardar nombre base para Excel
            base_filename = os.path.splitext(os.path.basename(mot_path[0]))[0]

            # Mostrar preview
            st.markdown("### Vista previa del DataFrame")
            st.dataframe(df.head(), hide_index=True)

            # Botón para descargar como Excel
            towrite = io.BytesIO()
            df.to_excel(towrite, index=False, engine="openpyxl")
            towrite.seek(0)

            st.download_button(
                label="📥 Descargar Excel",
                data=towrite,
                file_name=f"{base_filename}.xlsx",
                mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
            )

            # --- Mostrar el video si existe ---
            if mov_path:
                st.markdown("### 🎥 Video del ensayo")
                mov_file = zip_ref.open(mov_path[0])
                st.video(mov_file)

            # Selección de columnas para graficar
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
                    title="Curvas seleccionadas",
                    xaxis_title=df.columns[0],
                    yaxis_title="Valor",
                    template="plotly_white"
                )
                st.plotly_chart(fig, use_container_width=True)

            # --- Gráfico ángulo-ángulo ---
            st.markdown("---")
            st.markdown("### Gráfico Ángulo-Ángulo")

            col_angle_1, col_angle_2 = st.columns(2)
            eje_x = col_angle_1.selectbox("Columna eje X:", options=df.columns[1:], index=None)
            eje_y = col_angle_2.selectbox("Columna eje Y:", options=df.columns[1:], index=None)

            if eje_x and eje_y:
                fig = go.Figure()
                fig.add_trace(go.Scatter(
                    x=df[eje_x], y=df[eje_y], mode="lines", name=f"{eje_y} vs {eje_x}"
                ))
                fig.update_layout(
                    title=f"Ángulo–Ángulo ({eje_y} vs {eje_x})",
                    xaxis_title=eje_x,
                    yaxis_title=eje_y,
                    template="plotly_white",
                    yaxis=dict(scaleanchor="x", scaleratio=1)
                )
                st.plotly_chart(fig, use_container_width=True)
