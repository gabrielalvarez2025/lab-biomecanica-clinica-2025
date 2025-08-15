import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components


def main_marcha():
    st.title("Análisis de marcha")
    
    components.html(
    """
    <div class="sketchfab-embed-wrapper">
        <iframe title="Walk Cycle"
            frameborder="0"
            allowfullscreen
            mozallowfullscreen="true"
            webkitallowfullscreen="true"
            allow="autoplay; fullscreen; xr-spatial-tracking"
            xr-spatial-tracking
            execution-while-out-of-viewport
            execution-while-not-rendered
            web-share
            src="https://sketchfab.com/models/05c7560e49c1441aa0c70d3dc7bc710b/embed?transparent=1&ui_theme=dark"
            width="100%" height="600">
        </iframe>
        <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;">
            <a href="https://sketchfab.com/3d-models/walk-cycle-05c7560e49c1441aa0c70d3dc7bc710b"
               target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">
               Walk Cycle
            </a> by
            <a href="https://sketchfab.com/ekaant"
               target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">
               Niraj Ekaant
            </a> on
            <a href="https://sketchfab.com"
               target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">
               Sketchfab
            </a>
        </p>
    </div>
    """,
    height=650,
    )

