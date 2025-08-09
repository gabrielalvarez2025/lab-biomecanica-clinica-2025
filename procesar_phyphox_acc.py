import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main_phyphox():
    
    st.markdown("---")
    st.subheader("Procesando Datos del acelerómetro del celular con Phyphox")

    uploaded_file = st.file_uploader("Sube un archivo CSV", type=["csv"])

    if uploaded_file is not None:
        # Leer CSV (intenta con tabulador primero)
        try:
            df = pd.read_csv(uploaded_file, sep=",")
        except:
            df = pd.read_csv(uploaded_file, sep=",")

        # Limpiar nombres de columnas
        df.columns = df.columns.str.strip()

        st.write("Vista previa de los datos:")
        st.dataframe(df, hide_index=True)

        # Inputs para rango de tiempo
        min_time = float(0) #float(df["Time (s)"].min())
        max_time = float(df["Time (s)"].max())

        # Presentar graficos
        st.markdown(" ")
        st.markdown(" ")
        st.markdown("###  Representación gráfica de los datos:")

        esp1, col1, col2, esp2 = st.columns([20, 30, 30, 20])

        with col1:
            start_time = st.number_input("Tiempo inicial (s)", min_value=min_time, max_value=max_time, value=min_time, step=0.1)
        with col2:
            end_time = st.number_input("Tiempo final (s)", min_value=min_time, max_value=max_time, value=max_time, step=0.1)

        # Filtrar datos según rango seleccionado
        df_filtered = df[(df["Time (s)"] >= start_time) & (df["Time (s)"] <= end_time)]
        
        # Configuración de Seaborn y Matplotlib
        sns.set_theme(style="whitegrid", palette="pastel")

        # Crear figura con fondo transparente
        fig, ax = plt.subplots(figsize=(10, 6), facecolor="none")
        ax.set_facecolor("none")

        # Cambiar color de ejes y títulos a blanco
        ax.tick_params(colors="white")
        ax.xaxis.label.set_color("white")
        ax.yaxis.label.set_color("white")
        ax.title.set_color("white")

        # Graficar líneas
        sns.lineplot(x=df_filtered["Time (s)"], y=df_filtered["Acceleration x (m/s^2)"], label="Acc X", ax=ax)
        sns.lineplot(x=df_filtered["Time (s)"], y=df_filtered["Acceleration y (m/s^2)"], label="Acc Y", ax=ax)
        sns.lineplot(x=df_filtered["Time (s)"], y=df_filtered["Acceleration z (m/s^2)"], label="Acc Z", ax=ax)

        # Títulos
        ax.set_title("Aceleraciones en el Tiempo", fontsize=16)
        ax.set_xlabel("Tiempo (s)")
        ax.set_ylabel("Aceleración (m/s²)")

        # Fondo transparente también para la leyenda
        legend = ax.legend()
        legend.get_frame().set_facecolor("k")
        legend.get_frame().set_edgecolor("white")
        for text in legend.get_texts():
            text.set_color("white")

        # Mostrar gráfico en Streamlit
        st.pyplot(fig, transparent=True)
