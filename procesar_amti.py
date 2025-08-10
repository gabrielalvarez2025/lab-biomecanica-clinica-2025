import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main_forceplate():
    st.markdown("---")
    st.subheader("Procesando Datos de Plataforma de Fuerzas AMTI")

    uploaded_file = st.file_uploader("📂 Sube un archivo CSV con datos de plataforma AMTI", type=["csv"])

    if uploaded_file is not None:
        
        # Obtener freq de sampleo de celda row=2°, col=1°
        fs_row = pd.read_csv(uploaded_file, skiprows=1, nrows=1, header=None)
        freq_sampleo = fs_row.iloc[0, 0]  # Extraemos el valor fs
        
        # Intentamos leer el CSV, omitiendo las dos primeras filas de metadata
        df = pd.read_csv(uploaded_file, skiprows=3)
        df = df.iloc[:, 0:11] # solo datos plataforma, no EMG
        df.columns = df.columns.str.strip()  # limpiar nombres
        df = df.drop(0)

        
        
        st.write("Vista previa de los datos:")
        st.dataframe(df, hide_index=True)

        # Rango para Frame
        min_frame = int(df["Frame"].min())
        max_frame = int(df["Frame"].max())

        st.info(f"La frecuencia de sampleo fue de: {freq_sampleo}")

        st.markdown("#### Ajusta ventana de frames para graficar:")

        start_frame = st.number_input("Desde Frame:", min_value=min_frame, max_value=max_frame, value=min_frame, step=1)
        end_frame = st.number_input("Hasta Frame:", min_value=min_frame, max_value=max_frame, value=max_frame, step=1)

        df_filtered = df[(df["Frame"] >= start_frame) & (df["Frame"] <= end_frame)]

        st.markdown("### Selecciona las señales a graficar:")

        col_select_1, col_select_2, col_select_3 = st.columns(3)

        with col_select_1:
            st.markdown("###### Fuerzas:")
            show_Fx = st.checkbox("Fx (N)", True)
            show_Fy = st.checkbox("Fy (N)", True)
            show_Fz = st.checkbox("Fz (N)", True)
        
        with col_select_2:
            st.markdown("###### Torques:")
            show_Mx = st.checkbox("Mx (N mm)", False)
            show_My = st.checkbox("My (N mm)", False)
            show_Mz = st.checkbox("Mz (N mm)", False)
        
        with col_select_3:
            st.markdown("###### Posición del COP:")
            show_Cx = st.checkbox("Cx (mm)", False)
            show_Cy = st.checkbox("Cy (mm)", False)
            show_Cz = st.checkbox("Cz (mm)", False)

        # Lista de señales a graficar
        signals = []
        if show_Fx:
            signals.append(("Fx", "tab:blue"))
        if show_Fy:
            signals.append(("Fy", "tab:orange"))
        if show_Fz:
            signals.append(("Fz", "tab:green"))
        if show_Mx:
            signals.append(("Mx", "tab:red"))
        if show_My:
            signals.append(("My", "tab:purple"))
        if show_Mz:
            signals.append(("Mz", "tab:brown"))

        if not signals:
            st.warning("Selecciona al menos una señal para graficar.")
            return

        sns.set_theme(style="whitegrid")

        if show_Cx and show_Cy:
            st.markdown("### Estatocinesiograma (Trayectoria COP en el plano XY)")

            fig, ax = plt.subplots(figsize=(6, 6), facecolor="none")
            ax.set_facecolor("none")

            ax.tick_params(colors="black")
            ax.xaxis.label.set_color("black")
            ax.yaxis.label.set_color("black")
            ax.title.set_color("black")

            ax.plot(df_filtered["Cx"], df_filtered["Cy"], color="tab:red", marker=".", linestyle="-")
            ax.set_xlabel("Cx (mm)")
            ax.set_ylabel("Cy (mm)")
            ax.set_title("Estatocinesiograma")

            # Ajuste de aspecto para que X e Y tengan misma escala
            ax.set_aspect('equal', adjustable='datalim')

            st.pyplot(fig, transparent=True)
        
        for sig, color in signals:
            st.markdown(f"### Ajusta eje Y para {sig}")
            y_min = st.number_input(f"Mínimo eje Y ({sig})", value=float(df_filtered[sig].min()), key=f"ymin_{sig}")
            y_max = st.number_input(f"Máximo eje Y ({sig})", value=float(df_filtered[sig].max()), key=f"ymax_{sig}")

            fig, ax = plt.subplots(figsize=(10, 4), facecolor="none")
            ax.set_facecolor("none")

            ax.tick_params(colors="black")
            ax.xaxis.label.set_color("black")
            ax.yaxis.label.set_color("black")
            ax.title.set_color("black")

            sns.lineplot(x=df_filtered["Frame"], y=df_filtered[sig], ax=ax, color=color)

            ax.set_ylim(y_min, y_max)
            ax.set_title(f"{sig} en función del Frame", fontsize=14)
            ax.set_xlabel("Frame")
            ax.set_ylabel(sig)

            st.pyplot(fig, transparent=True)
        
        # Graficar Estatocinesiograma (trayectoria COP)

