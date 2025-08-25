import streamlit as st
import pandas as pd
import io
import plotly.graph_objects as go

def main_opencap():
    st.subheader("📊 Procesar archivo OpenCap (.txt)")

    uploaded_file = st.file_uploader("📂 Sube un archivo TXT exportado de OpenCap", type=["txt"])

    if uploaded_file is not None:
        st.success("✅ Archivo cargado")

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

        # Leer el txt como dataframe con separador de espacios
        df = pd.read_csv(data_buffer, delimiter=r"\s+", engine="python")

        # Renombrar columna de tiempo si existe
        if "time" in df.columns:
            df = df.rename(columns={"time": "Tiempo (s)"})

        # Mostrar preview
        st.markdown("### Vista previa del DataFrame")
        st.dataframe(df, hide_index=True)

        # --- Botón para descargar DataFrame como Excel ---
        st.markdown("---")
        st.markdown("### Descargar datos procesados")
        towrite = io.BytesIO()
        df.to_excel(towrite, index=False, engine='openpyxl')
        towrite.seek(0)

        st.download_button(
            label="📥 Descargar Excel",
            data=towrite,
            file_name="datos_opencap.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )

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

        
