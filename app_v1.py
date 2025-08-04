import streamlit as st
import matplotlib.pyplot as plt
import numpy as np

# Título
st.title("Diagrama de Cuerpo Libre: Fuerza Peso")

# Slider para cambiar la masa
masa = st.slider("Masa del objeto (kg)", min_value=1.0, max_value=20.0, step=0.5, value=5.0)

# Constante de gravedad
g = 9.81
fuerza_peso = masa * g

# Mostrar datos
st.markdown(f"**Fuerza peso (F = m·g):** {masa} kg × 9.81 m/s² = **{fuerza_peso:.2f} N**")

# Crear gráfico

fig, ax = plt.subplots()
ax.set_xlim(-1, 1)
ax.set_ylim(-fuerza_peso * 1.1, 10)
ax.axhline(0, color='black', linewidth=1)
ax.arrow(0, 0, 0, -fuerza_peso, head_width=0.1, head_length=5, fc='blue', ec='blue')
ax.text(0.1, -fuerza_peso/2, f'{fuerza_peso:.1f} N', color='blue')
ax.set_xlabel("x")
ax.set_ylabel("Fuerza (N)")
ax.set_title("Fuerza peso hacia abajo")
ax.grid(True)

st.pyplot(fig)
