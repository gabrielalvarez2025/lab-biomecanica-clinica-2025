import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from pydub import AudioSegment

def main_control_motor():
    st.markdown("#### Teorías del control motor")

    teorias = {
        "Teoría de la retroalimentación": "Esta teoría sugiere que el control"}