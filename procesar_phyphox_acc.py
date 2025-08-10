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

        col_A, col_B = st.columns(2)
        
        
        with col_A:

            bloq1, bloq2 = st.columns(2)

            with bloq1:
                show_x = st.checkbox("Acc Eje X", value=True)
                show_y = st.checkbox("Acc Eje Y", value=True)
            
            with bloq2:
                show_z = st.checkbox("Acc Eje Z", value=True)
                show_abs = st.checkbox("Acc absoluto", value=True)    
        
        with col_B:
            
            start_time = st.number_input("Mostrar tiempo **desde** el segundo:", min_value=min_time, max_value=max_time, value=min_time, step=0.1)
            end_time = st.number_input("Mostrar tiempo **hasta** el segundo:", min_value=min_time, max_value=max_time, value=max_time, step=0.1)



        # Filtrar datos
        df_filtered = df[(df["Time (s)"] >= start_time) & (df["Time (s)"] <= end_time)]

        st.markdown("### Selección de datos a graficar:")

        # Configuración de estilo
        sns.set_theme(style="whitegrid", palette="pastel")

        # Lista de ejes a mostrar
        selected_axes = []
        if show_x:
            selected_axes.append(("Acceleration x (m/s^2)", "#7EB87E", "Acc X"))
        if show_y:
            selected_axes.append(("Acceleration y (m/s^2)", "#6EBDE2", "Acc Y"))
        if show_z:
            selected_axes.append(("Acceleration z (m/s^2)",  "#B3B87E", "Acc Z"))
        if show_abs and "Absolute acceleration (m/s^2)" in df_filtered.columns:
            selected_axes.append(("Absolute acceleration (m/s^2)", "white", "Abs"))

        if not selected_axes:
            st.warning("Selecciona al menos una opción para graficar.")
            return

        # Dibujar cada gráfico por separado
        for col, color, label in selected_axes:
            fig, ax = plt.subplots(figsize=(10, 4), facecolor="none")
            ax.set_facecolor("none")

            # Cambiar colores del texto
            ax.tick_params(colors="white")
            ax.xaxis.label.set_color("white")
            ax.yaxis.label.set_color("white")
            ax.title.set_color("white")

            # Graficar
            sns.lineplot(x=df_filtered["Time (s)"], y=df_filtered[col], ax=ax, color=color)

            # Títulos
            ax.set_title(f"{label} en el Tiempo", fontsize=14)
            ax.set_xlabel("Tiempo (s)")
            ax.set_ylabel("Aceleración (m/s²)")

            st.pyplot(fig, transparent=True)
