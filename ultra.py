import streamlit as st
import pandas as pd
import gdown
import sqlite3
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
st.title("Bienvenido al Validador 🗂️")
st.sidebar.header("Menú de Navegación")

db_filename = "Base_Pacientes_NAL_BOT.bd"
file_id = "1o8CFlVb0HERuErdoNz6iXl9MMgzzQuvX"
url = f"https://drive.google.com/uc?id={file_id}"
gdown.download(url, db_filename, quiet=False)

conn = sqlite3.connect(db_filename)
consulta = st.text_input("Ingrese el número de identificación")

if consulta:
    if consulta.isdigit():  # Asegura que el ID es un número

        query_2 = "SELECT NOMBRE, TIPO_ID, PROGRAMA, CIUDAD FROM mi_tabla WHERE ID = ?"
        df_2 = pd.read_sql_query(query_2, conn, params=(consulta,))
        
        query = "SELECT PERIODO, VOLANTE, TRASLADOS_AUTORIZADOS, DISPONIBLES, COD_AXSEG, MIPRES, COORDINACIÓN FROM mi_tabla WHERE ID = ?"
        df = pd.read_sql_query(query, conn, params=(consulta,))

        query_3 = """
SELECT * 
FROM mi_tabla 
JOIN coordinacion 
ON mi_tabla.COORDINACIÓN = coordinacion.COORDINACIÓN
WHERE mi_tabla.COORDINACIÓN = ?
"""
        df_3 = pd.read_sql_query(query_3, conn, params=(consulta,))
        
        if df.empty:
            st.warning("No se encontraron resultados.")
        else:
            nombre = df_2["NOMBRE"].values[0]
            ciudad = df_2["CIUDAD"].values[0]
            tipo = df_2["TIPO_ID"].values[0]
            st.subheader(f"👤{tipo}-{consulta} | {nombre} | {ciudad}")
            #st.dataframe(df, use_container_width=True)
            st.dataframe(df_3, use_container_width=True)
    else:
        st.error("Por favor, ingrese un ID numérico válido.")
conn.close()


            # col1, col2, col3 = st.columns([1, 1, 1])
            # col1.markdown(f"👤 Nombre: {nombre}")  # Izquierda
            # col2.markdown(f"📍 Ciudad: {ciudad}")  # Centro
            # col3.markdown(f"🎓 Programa: {programa}")  # Derecha
            
