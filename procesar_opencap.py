import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main_opencap():

    st.markdown("---")
    st.subheader("📊 Procesando Datos de OpenCap")

    uploaded_file = st.file_uploader("📂 Sube un archivo CSV exportado de OpenCap", type=["csv", "txt"])

    if uploaded_file is not None:
        st.success("¡Excelente! Subiste exitosamente un archivo de OpenCap :)")

        # Leer el archivo, separado por espacios
        try:
            df = pd.read_csv(uploaded_file, delimiter=r"\s+", engine="python")
        except Exception as e:
            st.error(f"Error al leer archivo: {e}")
            return

        # Mostrar una vista previa
        st.markdown("### Vista previa de los datos:")
        st.dataframe(df.head(), hide_index=True)

        # Verificar columnas típicas de OpenCap
        st.markdown("### Columnas detectadas:")
        st.write(df.columns.tolist())

        # Si hay columna "time" la usamos
        if "time" in df.columns:
            df = df.rename(columns={"time": "Tiempo"})
        elif "frame" in df.columns:
            # Si solo hay "frame", lo transformamos en tiempo suponiendo 60 Hz
            df["Tiempo"] = df["frame"] / 60.0
        else:
            st.warning("No encontré columna de tiempo ni frame. Revisar CSV.")

        # Dejar Tiempo como primera columna
        cols = df.columns.tolist()
        if "Tiempo" in cols:
            cols = ["Tiempo"] + [c for c in cols if c != "Tiempo"]
            df = df[cols]

        # Mostrar tabla con tiempo
        st.markdown("### Datos con tiempo:")
        st.dataframe(df.head(), hide_index=True)

        st.markdown("---")
        st.markdown("### Selecciona variables a graficar:")

        # Checkboxes dinámicos
        selected_columns = st.multiselect("Elige variables para graficar", options=df.columns[1:], default=df.columns[1:3])

        if selected_columns:
            sns.set_theme(style="whitegrid")

            for col in selected_columns:
                st.markdown(f"#### {col} en función del Tiempo")

                y_min = float(df[col].min())
                y_max = float(df[col].max())

                ymin_input = st.number_input(f"Mínimo eje Y ({col})", value=y_min, key=f"ymin_{col}")
                ymax_input = st.number_input(f"Máximo eje Y ({col})", value=y_max, key=f"ymax_{col}")

                fig, ax = plt.subplots(figsize=(10, 4))
                sns.lineplot(x=df["Tiempo"], y=df[col], ax=ax)
                ax.set_ylim(ymin_input, ymax_input)
                ax.set_title(f"{col} en función del Tiempo", fontsize=14)
                ax.set_xlabel("Tiempo (s)")
                ax.set_ylabel(col)
                st.pyplot(fig)

        else:
            st.warning("Selecciona al menos una variable para graficar.")

