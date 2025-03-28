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
st.title("Validador UT Nuevo Renetur")
st.subheader("En este apartado podrás consultar las autorizaciones vigentes relacionadas con tu transporte especial")
st.sidebar.header("Menú de Navegación")

db_filename = "Base_Pacientes_NAL_BOT.bd"
file_id = "1o8CFlVb0HERuErdoNz6iXl9MMgzzQuvX"
url = f"https://drive.google.com/uc?id={file_id}"
gdown.download(url, db_filename, quiet=False)

conn = sqlite3.connect(db_filename)
consulta = st.text_input("Ingrese el número de identificación del **paciente**")

if consulta:
    if consulta.isdigit():  # Asegura que el ID es un número
        query = "SELECT PERIODO, VOLANTE, TRASLADOS_AUTORIZADOS, DISPONIBLES, COD_AXSEG, MIPRES, COORDINACIÓN FROM mi_tabla WHERE ID = ?"
        df = pd.read_sql_query(query, conn, params=(consulta,))

        query_2 = """
        SELECT
            mi_tabla.NOMBRE,
            mi_tabla.TIPO_ID,
            mi_tabla.PROGRAMA,
            mi_tabla.CIUDAD,
            coordinacion.Link
        FROM mi_tabla
        LEFT JOIN coordinacion
        ON mi_tabla.COORDINACIÓN = coordinacion.COORDINACIÓN
        WHERE mi_tabla.ID = ?
        """
        df_2 = pd.read_sql_query(query_2, conn, params=(consulta,))

        if df.empty:
            st.warning("No se encontraron resultados.")
        else:
            nombre = df_2["NOMBRE"].values[0]
            ciudad = df_2["CIUDAD"].values[0]
            tipo = df_2["TIPO_ID"].values[0]
            coord = df["COORDINACIÓN"].values[0]
            link = df_2["Link"].values[0]
            st.subheader(f"👤{tipo}-{consulta} | {nombre} | {ciudad}")
            st.dataframe(df, use_container_width=True) 
            st.markdown("💡**Muy bien hemos encontrado autorizaciones, si tienes traslados disponibles puedes agendar tus servicios. Si requieres que te apoye un gestor puedes usar los botones de contacto**")

            telefono = "573503836066"
            mensaje = "Hola perro quiero más información."
            mensaje_codificado = urllib.parse.quote(mensaje)  # Codifica caracteres especiales
            url_whatsapp = f"https://wa.me/{telefono}?text={mensaje_codificado}"
            
            col1, col2, col3 = st.columns([1, 1, 1])
            col1.link_button("📅 Solicitar Servicios",link, use_container_width=True)  # Izquierda
            col2.link_button("🗣️​ Atención Paciente en WhatsApp", url_whatsapp, use_container_width=True)  # Centro
            col3.link_button("📲 Contacto Coordinación en WhatsApp", url_whatsapp, use_container_width=True)  # Derecha

    else:
        st.error("Por favor, ingrese un ID numérico válido.")
conn.close()
