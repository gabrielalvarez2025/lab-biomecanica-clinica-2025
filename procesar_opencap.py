import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import io

def main_opencap():
    st.markdown("---")
    st.subheader("📊 Procesando Datos de OpenCap")

    uploaded_file = st.file_uploader("📂 Sube un archivo CSV exportado de OpenCap", type=["csv", "txt"])

    if uploaded_file is not None:
        st.success("¡Archivo cargado exitosamente! 🚀")

        # Leer todo el archivo como texto
        file_content = uploaded_file.getvalue().decode("utf-8").splitlines()

        # Buscar la línea "endheader"
        header_lines = 0
        for i, line in enumerate(file_content):
            if "endheader" in line:
                header_lines = i + 1   # saltar también la línea endheader
                break

        # Nos quedamos solo con los datos (sin encabezado)
        data_str = "\n".join(file_content[header_lines:])
        data_buffer = io.StringIO(data_str)

        # Leer CSV separado por espacios
        df = pd.read_csv(data_buffer, delimiter=r"\s+", engine="python")

        # Renombrar columna "time" si existe
        if "time" in df.columns:
            df = df.rename(columns={"time": "Tiempo (s)"})

        # Mostrar preview
        st.markdown("### Vista previa de los datos")
        st.dataframe(df.head(), hide_index=True)

        # Lista de columnas disponibles
        st.markdown("### Columnas detectadas")
        st.write(df.columns.tolist())

        # Selección de variables
        st.markdown("---")
        st.markdown("### Selecciona variables a graficar:")
        selected_columns = st.multiselect(
            "Elige variables (ej. pelvis_tilt, hip_flexion_r, knee_angle_r...)", 
            options=df.columns[1:], 
            default=["pelvis_tilt", "hip_flexion_r"]
        )

        if selected_columns:
            sns.set_theme(style="whitegrid")

            for col in selected_columns:
                st.markdown(f"#### {col} en función del tiempo")

                # Rango dinámico de Y
                y_min = float(df[col].min())
                y_max = float(df[col].max())
                ymin_input = st.number_input(f"Mínimo eje Y ({col})", value=y_min, key=f"ymin_{col}")
                ymax_input = st.number_input(f"Máximo eje Y ({col})", value=y_max, key=f"ymax_{col}")

                fig, ax = plt.subplots(figsize=(10, 4))
                sns.lineplot(x=df["Tiempo (s)"], y=df[col], ax=ax)
                ax.set_ylim(ymin_input, ymax_input)
                ax.set_title(f"{col} en función del tiempo", fontsize=14)
                ax.set_xlabel("Tiempo (s)")
                ax.set_ylabel(col)
                st.pyplot(fig)

        else:
            st.warning("Selecciona al menos una variable para graficar.")
