import streamlit as st
import pandas as pd
import io

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
                header_lines = i + 1   # cortamos incluyendo esa línea
                break

        # Nos quedamos solo con los datos (desde después de endheader)
        data_str = "\n".join(file_content[header_lines:])
        data_buffer = io.StringIO(data_str)

        # Leer el txt como dataframe con separador de espacios múltiples
        df = pd.read_csv(data_buffer, delimiter=r"\s+", engine="python")

        # Renombrar columna de tiempo si existe
        if "time" in df.columns:
            df = df.rename(columns={"time": "Tiempo (s)"})

        # Mostrar preview
        st.markdown("### Vista previa del DataFrame")
        st.dataframe(df.head(), hide_index=True)

        # Mostrar lista de columnas
        st.markdown("### Columnas detectadas:")
        st.write(df.columns.tolist())
