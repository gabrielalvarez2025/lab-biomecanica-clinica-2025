import streamlit as st
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit.components.v1 as components


def main_marcha():
    st.title("Análisis de marcha")

    embeded_model_1 = """
    <div class="sketchfab-embed-wrapper">
        <iframe title="skeleton walk cycle"
            frameborder="0"
            allowfullscreen
            mozallowfullscreen="true"
            webkitallowfullscreen="true"
            allow="autoplay; fullscreen; xr-spatial-tracking"
            xr-spatial-tracking
            execution-while-out-of-viewport
            execution-while-not-rendered
            web-share
            src="https://sketchfab.com/models/cc2d23e91414469ea983dddf46c03863/embed?autospin=1&autostart=1&preload=1&transparent=1&ui_theme=dark"
            width="100%" height="600">
        </iframe>
        <p style="font-size: 13px; font-weight: normal; margin: 5px; color: #4A4A4A;">
            <a href="https://sketchfab.com/3d-models/skeleton-walk-cycle-cc2d23e91414469ea983dddf46c03863"
               target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">
               skeleton walk cycle
            </a> by
            <a href="https://sketchfab.com/AngelsDemons"
               target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">
               Angels&amp;Demons
            </a> on
            <a href="https://sketchfab.com"
               target="_blank" rel="nofollow" style="font-weight: bold; color: #1CAAD9;">
               Sketchfab
            </a>
        </p>
    </div>
    """

    components.html(embeded_model_1, height=650)


