import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.signal import butter, filtfilt   # 👈 importar

# --------------------------
# Filtro Butterworth
# --------------------------
def butterworth_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    y = filtfilt(b, a, data)
    return y


def main_phyphox():
    st.markdown("---")
    st.subheader("Procesando Datos del acelerómetro del celular con Phyphox")

    uploaded_file = st.file_uploader("📂 Sube un archivo CSV", type=["csv"])

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

        # Calcular mean acc de cada eje
        acc_g = 9.8  # m/s2
        avg_abs = {
            "X": df["Acceleration x (m/s^2)"].abs().mean(),
            "Y": df["Acceleration y (m/s^2)"].abs().mean(),
            "Z": df["Acceleration z (m/s^2)"].abs().mean()
        }
        eje_vertical = min(avg_abs, key=lambda eje: abs(avg_abs[eje] - acc_g))

        st.markdown("---")
        st.markdown("### Graficando tus datos:")
        
        col_A, col_B = st.columns(2)
        
        with col_A:
            st.markdown("###### Selecciona los datos que quieres graficar:")
            col_mostrar_ejes1, col_mostrar_ejes2 = st.columns([30, 65])
            with col_mostrar_ejes1:
                show_x = st.checkbox("Acc Eje X", value=True)
                show_y = st.checkbox("Acc Eje Y", value=True)
                show_z = st.checkbox("Acc Eje Z", value=True)
            with col_mostrar_ejes2:
                show_abs = st.checkbox("Acc absoluta (X + Y + Z)", value=False)
                
        with col_B:
            st.markdown("###### ¿Quieres quitar la acc de gravedad?")
            restar_g = st.checkbox(f"Restar g = 9,8 m/s² de la acc vertical (eje {eje_vertical})", value=True)

            st.markdown("###### ¿Quieres aplicar un filtro a la señal?")
            filtrar_check = st.checkbox("Filtrar señal con Butterworth", value=False)

            if filtrar_check:
                cutoff = st.number_input("Frecuencia de corte (Hz)", min_value=0.1, value=5.0, step=0.1)
                orden = st.slider("Orden del filtro Butterworth", min_value=1, max_value=10, value=4)
            else:
                cutoff, orden = None, None

        st.markdown(" ")
        st.markdown("###### Puedes ajustar la ventana de tiempo que te interesa mirar:")

        esp_t_izq, col_tiempo1, esp_t_ed, col_tiempo2, esp_t_der = st.columns([10, 30, 60, 30, 15])
        with col_tiempo1:
            start_time = st.number_input("**Desde** (seg):", min_value=min_time, max_value=max_time, value=min_time, step=0.1)
        with col_tiempo2:
            end_time = st.number_input("**Hasta** (seg):", min_value=min_time, max_value=max_time, value=max_time, step=0.1)
        
        # Filtrar datos por tiempo
        df_filtered = df[(df["Time (s)"] >= start_time) & (df["Time (s)"] <= end_time)].copy()

        # Restar gravedad si está activado
        if restar_g:
            col_map = {"X": "Acceleration x (m/s^2)",
                       "Y": "Acceleration y (m/s^2)",
                       "Z": "Acceleration z (m/s^2)"}
            vertical_col = col_map[eje_vertical]
            df_filtered[vertical_col] = df_filtered[vertical_col] - (
                9.8 if df_filtered[vertical_col].mean() > 0 else -9.8
            )

        # Configuración de estilo
        sns.set_theme(style="whitegrid", palette="pastel")

        # Lista de ejes a mostrar
        selected_axes = []
        if show_x:
            selected_axes.append(("Acceleration x (m/s^2)", "#7EB87E", f"Acc X"))
        if show_y:
            selected_axes.append(("Acceleration y (m/s^2)", "#6EBDE2", f"Acc Y"))
        if show_z:
            selected_axes.append(("Acceleration z (m/s^2)",  "#B3B87E", f"Acc Z"))
        if show_abs and "Absolute acceleration (m/s^2)" in df_filtered.columns:
            selected_axes.append(("Absolute acceleration (m/s^2)", "white", "Aceleración absoluta"))

        if not selected_axes:
            st.warning("Selecciona al menos una opción para graficar.")
            return

        # Dibujar cada gráfico por separado
        for col, color, label in selected_axes:
            
            # 👉 Aplicar filtro si está activado
            if filtrar_check and cutoff is not None and orden is not None:
                try:
                    fs = 1 / (df_filtered["Time (s)"].iloc[1] - df_filtered["Time (s)"].iloc[0])
                    df_filtered[col] = butterworth_filter(df_filtered[col], cutoff=cutoff, fs=fs, order=orden)
                except Exception as e:
                    st.error(f"No se pudo aplicar el filtro en {label}: {e}")

            col_plot1, col_plot2 = st.columns([90, 10])
            with col_plot2:
                y_max = st.number_input(" ", value=float(df_filtered[col].max()), step=0.5, key=f"ymax_{col}")
                st.markdown("max ↑")
                st.markdown(" ")
                st.markdown(" ")
                st.markdown(" ")
                st.markdown(" ")
                y_min = st.number_input(f"min ↓", value=float(df_filtered[col].min()), step=0.5, key=f"ymin_{col}")
            
            with col_plot1:
                fig, ax = plt.subplots(figsize=(10, 4), facecolor="none")
                ax.set_facecolor("none")

                ax.tick_params(colors="white")
                ax.xaxis.label.set_color("white")
                ax.yaxis.label.set_color("white")
                ax.title.set_color("white")

                sns.lineplot(x=df_filtered["Time (s)"], y=df_filtered[col], ax=ax, color=color)

                ax.set_ylim(y_min, y_max)
                ax.set_title(f"{label} en el Tiempo", fontsize=14)
                ax.set_xlabel("Tiempo (s)")
                ax.set_ylabel("Aceleración (m/s²)")

                st.pyplot(fig, transparent=True)
