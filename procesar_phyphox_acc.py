import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main_phyphox():
    
    st.markdown("---")
    st.subheader("Procesando Datos del acelerómetro del celular con Phyphox")

    uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

    if uploaded_file is not None:
        # Leer CSV
        try:
            df = pd.read_csv(uploaded_file, sep=",")
        except:
            df = pd.read_csv(uploaded_file, sep=",")

        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip()

        st.write("Vista previa de los datos:")
        st.dataframe(df, hide_index=True)

        # Inputs para rango de tiempo
        min_time = float(0)
        max_time = float(df["Time (s)"].max())

        esp1, col1, col2, esp2 = st.columns([20, 30, 30, 20])
        with col1:
            start_time = st.number_input("Tiempo inicial (s)", min_value=min_time, max_value=max_time, value=min_time, step=0.1)
        with col2:
            end_time = st.number_input("Tiempo final (s)", min_value=min_time, max_value=max_time, value=max_time, step=0.1)

        # Filtrar datos
        df_filtered = df[(df["Time (s)"] >= start_time) & (df["Time (s)"] <= end_time)]

        # Configuración de Seaborn
        sns.set_theme(style="whitegrid", palette="pastel")

        # Función para graficar cada eje
        def plot_acc(axis_label, color=None):
            fig, ax = plt.subplots(figsize=(10, 4), facecolor="none")
            ax.set_facecolor("none")
            
            # Estilo de texto blanco
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")

            sns.lineplot(x=df_filtered["Time (s)"], y=df_filtered[axis_label], ax=ax, color=color)
            
            ax.set_title(f"{axis_label} en el Tiempo", fontsize=14)
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel("Aceleración (m/s²)")

            st.pyplot(fig, transparent=True)

        # Graficar cada componente
        plot_acc("Acceleration x (m/s^2)")
        plot_acc("Acceleration y (m/s^2)")
        plot_acc("Acceleration z (m/s^2)")

        st.markdown("hola")
