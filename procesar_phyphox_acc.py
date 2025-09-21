import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from scipy.signal import butter, filtfilt   # 👈 importar
import plotly.graph_objects as go   # 👈 agregar import


# --------------------------
# Filtro Butterworth
# --------------------------
def butterworth_filter(data, cutoff, fs, order=4):
    nyquist = 0.5 * fs
    normal_cutoff = cutoff / nyquist
    b, a = butter(order, normal_cutoff, btype="low", analog=False)
    y = filtfilt(b, a, data)
    return y

def butterworth_filter_bandpass(data, fs, order=4, low_cut=None, high_cut=None):
    """
    Aplica un filtro Butterworth:
    - low_cut: frecuencia de corte inferior (Hz)
    - high_cut: frecuencia de corte superior (Hz)
    """
    nyquist = 0.5 * fs

    if low_cut and high_cut:
        # Filtro pasa banda
        normal_cutoff = [low_cut/nyquist, high_cut/nyquist]
        btype = "band"
    elif low_cut:
        normal_cutoff = low_cut / nyquist
        btype = "high"
    elif high_cut:
        normal_cutoff = high_cut / nyquist
        btype = "low"
    else:
        # Sin filtro
        return data

    b, a = butter(order, normal_cutoff, btype=btype, analog=False)
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
                # 👉 Plotly en lugar de Matplotlib
                fig = go.Figure()

                fig.add_trace(go.Scatter(
                    x=df_filtered["Time (s)"],
                    y=df_filtered[col],
                    mode="lines",
                    line=dict(color=color, width=2),
                    name=label
                ))

                # Ajustar límites del eje Y
                fig.update_yaxes(range=[y_min, y_max], title="Aceleración (m/s²)")
                fig.update_xaxes(title="Tiempo (s)")

                # Estilo general
                fig.update_layout(
                    title=f"{label} en el Tiempo",
                    plot_bgcolor="rgba(0,0,0,0)",
                    paper_bgcolor="rgba(0,0,0,0)",
                    font=dict(color="white"),
                    margin=dict(l=40, r=20, t=40, b=40),
                    height=400
                )

                st.plotly_chart(fig, use_container_width=True)

def ejemplo_fr_botas():
    """
    Ejemplo de uso de phyphox:
    - Col1: gif de un gato o mensaje
    - Col2: gráfico interactivo del eje Z (sin gravedad),
            filtrado con Butterworth con parámetros ajustables
    """

    st.set_page_config(layout="wide")

    st.markdown("---")
    st.markdown("##### Ejemplo 1: Midiendo la frecuencia respiratoria de un gato usando el celular")

    col_web_left, col_web_esp, col_web_right = st.columns([48, 4, 48])
    proporcion = [35, 65]

    
    espacio = st.markdown(" ")

    with col_web_left:

        st.markdown("Veamos un ejemplo de un escenario doméstico en el que podríamos usar un celular para capturar señales biológicas y así complementar una evaluación clínica.")
        
        col_img_botas, col_caso = st.columns(proporcion)

        col_text1, col_gif = st.columns([70, 30])
        
        col_text2, col_plot = st.columns(proporcion)

        

        st.markdown(" ")
        st.markdown(" ")

        col_calculo_fr1, col_calculo_fr2 = st.columns(2)
    
    
    with col_web_right:
        
        st.markdown("##### Filtrando la señal")
        st.markdown('Te habrás dado cuenta que en el gráfico distinguimos la "señal original", (en blanco) de la "señal filtrada" (en naranjo). Esto se debe a que aplicamoos uno de los posibles pasos de procesamiento de señales a la señal de aceleración capturada: el filtrado.')
        col_text_filter, col_sliders = st.columns(2)

        

   
        

    with col_img_botas:
        
        st.markdown("Este es Botas")
        st.image("img_botas.png", use_container_width=True)
        #st.image("cat3.gif", use_container_width=True)

    with col_caso:
        
        st.markdown(" ")
        st.markdown(" ")
        st.markdown("Botas tiene asma y su veterinaria nos ha pedido que una vez a la semana monitoreemos su frecuencia respiratoria (FR) de reposo en casa.")
        st.markdown("Para hacer esto, debemos esperar a que esté quieto y tranquilo, y con un cronómetro, contar sus respiraciones en un minuto. Es decir, una evaluación sencilla.")
        st.markdown("Sin embargo, como estudiante de Kinesiología que está cursando su ramo de Análisis de Movimiento y aprendiendo a usar bioinstrumentos, te preguntas... ¿podemos complementar esta evaluación con un registro más objetivo? ¿Podemos usar algún bioinstrumento casero para cuantificar su FR?")
        
        
    with col_gif:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.image("cat3.gif", use_container_width=True)

    with col_text1:
        st.markdown("Con el objetivo de medir su frecuencia respiratoria en reposo de forma más exacta, te propones usar el acelerómetro de tu celular.")
        st.markdown("Si colocas el celular sobre su tórax mientras duerme, este se moverá hacia arriba y abajo con cada respiración. Este movimiento es sensado como aceleración por el acelerómetro del celular.")
        st.markdown("Si capturamos la aceleración lineal del celular en el eje vertical (eje Z), podemos observar las oscilaciones causadas por el tórax de Botas con cada ciclo respiratorio.")
        

    with col_text2:
        
        st.markdown("En la señal (arriba), deberíamos ver un patrón de acelerometría que se repite en ciclos. Si contamos cuántos ciclos hay en un minuto, podemos calcular su frecuencia respiratoria.")
        
        
        

    with col_calculo_fr2:
        st.image("img_capture_plot_cat_fr.png", use_container_width=True)

    with col_calculo_fr1:
        st.markdown("También podemos contar los ciclos en 15 segundos y luego multiplicar por 4 para hacer una estimación rápida.")
        st.markdown("##### Analicemos:")
        st.markdown("Ya observaste y mediste; estás en la 3° etapa de evaluación: análisis.")
        st.markdown("¿Cuál es la frecuencia respiratoria de Botas?")
        st.markdown("Considerando que el rango de FR en reposo normal para un gato es 20 a 30 rpm, ¿qué podría estar pasando con Botas?")
        
        

    # Leer el CSV de ejemplo
    try:
        df = pd.read_csv("ejemplo_data_acc_phyphox_fr_botas.csv", sep=",")
    except FileNotFoundError:
        st.error("No se encontró el archivo 'ejemplo_data_acc_phyphox_fr_botas.csv'.")
        return

    df.columns = df.columns.str.strip()

    # Preparar columna Z sin gravedad
    if "Acceleration z (m/s^2)" not in df.columns:
        st.error("El CSV no tiene la columna 'Acceleration z (m/s^2)'.")
        return

    df["Acceleration z (m/s^2) [no g]"] = df["Acceleration z (m/s^2)"] - 9.8

    t = df["Time (s)"]
    z = df["Acceleration z (m/s^2) [no g]"]

    # Calcular frecuencia de muestreo
    fs = 1 / (t.iloc[1] - t.iloc[0])
    
    
    with col_text_filter:
        st.markdown("Cuando capturamos señales usando sensores, es común que haya ruido contaminando la señal. Ruido es todo aquello que no es parte de la señal que queremos medir.")
        st.markdown("En este caso, queremos medir las oscilaciones causadas por la respiración, pero al mismo tiempo sensamos otras fuentes de movimiento, que generan ruido en la señal. Por ejemplo, cada vez que Botas respira, ronronea. Esa vibración genera movimiento que contamina la señal que queremos medir.")
        st.markdown("Para eliminar ruido de una señal, podemos usar un **filtro digital**.")
        st.markdown("Un filtro digital es un algoritmo que procesa la señal en términos de las frecuencias que la componen y, al igual que un colador, deja pasar solo las frecuencias que nos interesan, ignorando las demás.")
        st.markdown("Existen muchos tipos de filtros digitales. En este ejemplo, usaremos un filtro 'de pasa banda', es decir, un filtro que deja pasar sólo un rango de frecuencias que nosotros seleccionamos.")
        
    
    with col_sliders:
        #st.markdown("¡Mira qué bonito! --")

        
        
        st.markdown("La respiración en reposo se repite pocas veces por segundo (20 a 30 rpm en un gato), por lo que ocurre a una frecuencia baja (0.3 a 0.4 Hz). En cambio, el ronroneo ocurre a una frecuencia más alta (p.ej. 25 Hz).")
        st.markdown("Por lo tanto, para limpiar nuestra señal, podemos usar un filtro que deje pasar las frecuencias bajas (ej. FR), pero bloquee las frecuencias altas (ej. ronroneo).")
        
        st.markdown("En el gráfico que viste, la señal original (ruidosa) está en blanco y la filtrada (limpia) en naranjo. Decidimos filtrar la señal dejando pasar sólo las frecuencias entre 0 Hz a 10 Hz, y bloqueando todas las demás hacia derecha y hacia izquierda. A nuestro criterio, vimos que estos parámetros permiten visualizar bien los ciclos respiratorios, pues la FR es un fenómeno de frecuencias más bien bajas.")
        
        st.markdown("Abajo, puedes deslizar los sliders para jugar con los parámetros del filtro, elegir otros, y así ver cómo estos cambios afectan la señal filtrada (naranjo).")
        
        
        # -----------------------
        # Inputs interactivos para filtro
        # -----------------------
        st.markdown("##### Ajusta aquí el filtro digital")
        low_cut, high_cut = st.slider(
            "Elige la banda de frecuencias (Hz) que dejarás pasar:",
            min_value=0.0,
            max_value=float(fs/2)/2,
            value=(0.0, 10.0),  # valores por defecto: low=0, high=10
            step=0.1
        )
        orden = st.slider("Orden del filtro", min_value=1, max_value=5, value=5)

    with col_plot:
        
        

        
        
        st.markdown("⤹ <small>Presiona la leyenda para ocultar/mostrar las curvas</small>", unsafe_allow_html=True)
        # Aplicar filtro pasa banda
        z_filt = butterworth_filter_bandpass(z, fs=fs, order=orden, low_cut=low_cut, high_cut=high_cut)
        #0, 10, 1

        # Crear gráfico interactivo con Plotly
        fig = go.Figure()

        # Señal original en gris
        fig.add_trace(go.Scatter(
            x=t, y=z,
            mode="lines",
            line=dict(color="lightgray", width=0.7),
            name="Señal original"
        ))

        # Señal filtrada en naranjo
        fig.add_trace(go.Scatter(
            x=t, y=z_filt,
            mode="lines",
            line=dict(color="#FFA500", width=1.5),
            name=f"Señal filtrada (cutoff = ( {round(low_cut, 2)} , {round(high_cut, 2)} ) Hz, orden {orden})"
        ))

        fig.update_layout(
            title=" ",
            xaxis_title="Tiempo (s)",
            yaxis_title="Aceleración (m/s²)",
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            font=dict(color="white"),
            margin=dict(l=40, r=20, t=60, b=40),  # un poco más de margen arriba para la leyenda
            height=400,
            legend=dict(
                orientation="h",
                yanchor="bottom",
                y=1.02,
                xanchor="center",
                x=0.5
            )
        )

        # 👉 Rango inicial de ejes
        fig.update_xaxes(range=[2.5, 20])
        fig.update_yaxes(range=[-1.5, 0.5])
        
        st.plotly_chart(fig, use_container_width=True)

        
