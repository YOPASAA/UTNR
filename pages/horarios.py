import streamlit as st
import pandas as pd
import gdown
import sqlite3
import urllib.parse
import os
import time

st.set_page_config(
    page_title="Asistente UTNR",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://miweb.com/ayuda"
        # "Report a bug": "https://miweb.com/soporte",
        # "About": "Aplicación de análisis de ventas creada con Streamlit 🚀"
    }
)

st.sidebar.header("Menú de Navegación")


col1,col2 = st.columns([1,8])
with col1:
    st.image("Imagen1.png", width=150)  
with col2:
    st.write("")  # Espacio en blanco
    st.title("Pagina 2 perra")

