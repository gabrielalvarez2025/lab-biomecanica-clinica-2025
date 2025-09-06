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

        header_row = pd.read_csv(
            uploaded_file,
            skiprows=5,
            nrows=1,
            header=None,
            engine="python",
            delimiter=";"
        )
        st.dataframe(header_row, hide_index=True)

        # Resetear el puntero del archivo
        uploaded_file.seek(0)

        # Leer datos omitiendo las primeras filas de metadatos
        df = pd.read_csv(
            uploaded_file,
            skiprows=7,
            header=None,
            engine="python",
            delimiter=";"
        )

        # Eliminar las últimas 22 columnas
        df = df.iloc[1:, :-22]

        # Asignar headers, permitiendo duplicados con sufijos m1, m2...
        counts = {}
        new_cols = []
        for col in header_row.iloc[0, :df.shape[1]]:
            col_clean = col.strip()
            if col_clean not in counts:
                counts[col_clean] = 1
                new_cols.append(col_clean)
            else:
                counts[col_clean] += 1
                new_cols.append(f"{col_clean} m{counts[col_clean]}")
        df.columns = new_cols

        

        st.markdown("### Vista previa de tus datos:")
        st.dataframe(df, hide_index=True)

        
        # --- Separar gran dataframe df en df pequeños por variable ---
        
        dfs_pequeños = [] # Lista donde se guardarán los DataFrames pequeños

        n_cols = int(df.shape[1])
        
        # Iterar de 0 hasta el número total de columnas, de 2 en 2
        df_var1 = df.iloc[:, 0:1]  # Tomar 2 columnas a la vez
        

        st.dataframe(df_var1, hide_index=True)  # Mostrar el primer DataFrame pequeño como ejemplo

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
