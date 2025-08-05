import streamlit as st
import pyvista as pv
from stpyvista import stpyvista

def mostrar():
    
    
    st.header("Unidad 5: Análisis de marcha")

    # Cargar y mostrar modelo 3D
    plotter = pv.Plotter()
    plotter.add_mesh(pv.read("modelo.glb"))  # usa .glb o .gltf convertido desde .fbx

    stpyvista(plotter)

    