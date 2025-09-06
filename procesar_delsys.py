import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main_delsys():
    st.markdown("---")
    st.subheader("Procesando Datos EMG/IMU Delsys")

    uploaded_file = st.file_uploader("📂 Sube un archivo CSV de Delsys", type=["csv"])

    if uploaded_file is not None:
        st.success("¡Archivo CSV de Delsys cargado exitosamente! ✅")

        # Leer CSV completo sin saltar filas
        df = pd.read_csv(uploaded_file, sep=";", header=None, dtype=str)

        # Eliminar filas de metadatos: filas 0 a 6 (Python index 0-6)
        df = df.drop([0,1,2,3,4,5,6]).reset_index(drop=True)

        # Asignar fila 7 (original fila 7 en Excel) como encabezados
        df.columns = df.iloc[0]  # fila 7 ahora es la fila 0 después del drop
        df = df.drop(0).reset_index(drop=True)

        # Convertir columnas numéricas a float (reemplazar ',' por '.')
        for col in df.columns:
            df[col] = df[col].str.replace(",", ".").astype(float, errors='ignore')

        st.markdown("### Vista previa de tus datos:")
        st.dataframe(df, hide_index=True)

        # Separar grupos de señales
        imu_cols = [c for c in df.columns if "ACC" in c or "GYRO" in c]
        emg_cols = [c for c in df.columns if "EMG" in c]

        st.markdown("---")
        st.markdown("### Selecciona qué señales visualizar")

        tab1, tab2 = st.tabs(["📈 IMU (ACC/GYRO)", "💪 EMG"])

        with tab1:
            if imu_cols:
                selected_imu = st.multiselect("Selecciona canales IMU", options=imu_cols, default=imu_cols[:2])
                if selected_imu:
                    for sig in selected_imu:
                        fig, ax = plt.subplots(figsize=(10, 4))
                        sns.lineplot(x=df.index, y=df[sig], ax=ax)
                        ax.set_title(f"{sig} en función del Tiempo (aprox)")
                        ax.set_xlabel("Muestras")
                        ax.set_ylabel(sig)
                        st.pyplot(fig)
            else:
                st.warning("No se encontraron columnas IMU en el archivo.")

        with tab2:
            if emg_cols:
                selected_emg = st.multiselect("Selecciona canales EMG", options=emg_cols, default=emg_cols[:2])
                if selected_emg:
                    for sig in selected_emg:
                        fig, ax = plt.subplots(figsize=(10, 4))
                        sns.lineplot(x=df.index, y=df[sig], ax=ax)
                        ax.set_title(f"{sig} en función del Tiempo (aprox)")
                        ax.set_xlabel("Muestras")
                        ax.set_ylabel(sig)
                        st.pyplot(fig)
            else:
                st.warning("No se encontraron columnas EMG en el archivo.")
