import streamlit as st
import pandas as pd
import gdown
import sqlite3
# import urllib.parse
# import os
# import time
st.set_page_config(layout="wide")
                   
db_filename = "Base_Pacientes_NAL_BOT.bd"
file_id = "1o8CFlVb0HERuErdoNz6iXl9MMgzzQuvX"
url = f"https://drive.google.com/uc?id={file_id}"
gdown.download(url, db_filename, quiet=False)
conn = sqlite3.connect(db_filename)

col1,col2 = st.columns([1,8])
with col1:
    st.image("Imagen1.png", width=100)  
with col2:
    # st.write("")  # Espacio en blanco
    st.title("Nuestros Horarios")

col1,col2,col3 = st.columns([5,1,5])
with col1:
    st.title("Atención al Usuario 🗣")
    st.subheader("Nuestros canales de atención estan disponibles de lunes a viernes de 8am a 4pm días hábiles.")
    query = "SELECT COORDINACIÓN, CEL, Cobertura FROM coordinacion"
    df = pd.read_sql_query(query, conn)
    st.write("Puedes hacer contacto vía WhatsApp con nuestras coordinaciónes:")

    for _, row in df.iterrows():
        numero = row["CEL"]
        coordinacion = row["COORDINACIÓN"]
        cobertura = row["Cobertura"]
        url_whatsapp = f"https://wa.me/{numero.replace('+', '')}"
        st.link_button(f"{coordinacion}: {cobertura}",url_whatsapp, use_container_width=True)
    conn.close()
    
with col2:
    st.write("")
with col3:
    st.title("Solicitud Servicios 📝 (formulario)")
    st.subheader("Nuestro formulario recibira tus solicitudes de servicios de lunes a viernes de 1:00 hrs (1am) a 14:00 hrs (2pm)")
    st.write("Puedes acceder a tu formulario consultando con la pagina principal")
    
