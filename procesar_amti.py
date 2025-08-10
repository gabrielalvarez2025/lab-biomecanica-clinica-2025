import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

def main_forceplate():
    st.markdown("---")
    st.subheader("Procesando Datos de Plataforma de Fuerzas AMTI")

    uploaded_file = st.file_uploader("📂 Sube un archivo CSV con datos de plataforma AMTI", type=["csv"])

    if uploaded_file is not None:
        df = pd.read_csv(uploaded_file, skiprows=3)
        df = df.iloc[:, 0:11]  # Solo columnas relevantes (incluye Cx y Cy)
        df.columns = df.columns.str.strip()
        df = df.drop(0)  # Quitar fila índice 0 (posible fila residual)

        st.write("Vista previa de los datos:")
        st.dataframe(df, hide_index=True)

        min_frame = int(df["Frame"].min())
        max_frame = int(df["Frame"].max())

        st.markdown("#### Ajusta ventana de frames para graficar:")
        start_frame = st.number_input("Desde Frame:", min_value=min_frame, max_value=max_frame, value=min_frame, step=1)
        end_frame = st.number_input("Hasta Frame:", min_value=min_frame, max_value=max_frame, value=max_frame, step=1)

        df_filtered = df[(df["Frame"] >= start_frame) & (df["Frame"] <= end_frame)]

        # Verificar que existan columnas Cx y Cy
        if "Cx" in df_filtered.columns and "Cy" in df_filtered.columns:
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

            ax.set_aspect('equal', adjustable='datalim')

            st.pyplot(fig, transparent=True)
        else:
            st.warning("No se encontraron las columnas 'Cx' y 'Cy' para graficar el estatocinesiograma.")
