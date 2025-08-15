import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components


def main_marcha():
    st.title("Análisis de marcha")

    embedded_code = f"""
    <div class="sketchfab-embed-wrapper"> <iframe title="Walk Cycle" frameborder="0" allowfullscreen mozallowfullscreen="true" webkitallowfullscreen="true" allow="autoplay; fullscreen; xr-spatial-tracking" xr-spatial-tracking execution-while-out-of-viewport execution-while-not-rendered web-share width="640" height="480" src="https://sketchfab.com/models/05c7560e49c1441aa0c70d3dc7bc710b/embed?autostart=1&preload=1&transparent=1&ui_hint=0&ui_theme=dark"> </iframe> <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;"> <a href="https://sketchfab.com/3d-models/walk-cycle-05c7560e49c1441aa0c70d3dc7bc710b?utm_medium=embed&utm_campaign=share-popup&utm_content=05c7560e49c1441aa0c70d3dc7bc710b" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> Walk Cycle </a> by <a href="https://sketchfab.com/ekaant?utm_medium=embed&utm_campaign=share-popup&utm_content=05c7560e49c1441aa0c70d3dc7bc710b" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;"> Niraj Ekaant </a> on <a href="https://sketchfab.com?utm_medium=embed&utm_campaign=share-popup&utm_content=05c7560e49c1441aa0c70d3dc7bc710b" target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">Sketchfab</a></p></div>
    """

    components.html(embedded_code, height=650)
