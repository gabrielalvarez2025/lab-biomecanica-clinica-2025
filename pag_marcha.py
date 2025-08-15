import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components


def main_marcha():
    st.title("Análisis de marcha")
    
    components.html(
    '<iframe src="https://sketchfab.com/3d-models/walk-cycle-05c7560e49c1441aa0c70d3dc7bc710b" width="100%" height="600" allowfullscreen></iframe>',
    height=600
)

