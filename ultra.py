import streamlit as st
import pandas as pd
import gdown
import sqlite3
import urllib.parse
import os
import time

st.set_page_config(
    page_title="Validación UTNR",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        "Get Help": "https://miweb.com/ayuda"
        # "Report a bug": "https://miweb.com/soporte",
        # "About": "Aplicación de análisis de ventas creada con Streamlit 🚀"
    }
)
st.sidebar.title("Menú de Navegación")
col1,col2 = st.columns([1,8])
with col1:
    st.image("Imagen1.png", width=100)  
with col2:
    st.title("Validador UT Nuevo Renetur")

st.info("En este espacio podras consultar si cuentas con autorizaciones vigentes para tu transporte con nosotros, **Nuevo Renetur**.")

db_filename = "Base_Pacientes_NAL_BOT.bd"
file_id = "1o8CFlVb0HERuErdoNz6iXl9MMgzzQuvX"
url = f"https://drive.google.com/uc?id={file_id}"
gdown.download(url, db_filename, quiet=False)
conn = sqlite3.connect(db_filename)

if "consulta_realizada" not in st.session_state:
    st.session_state.consulta_realizada = False

col1, col2, col3 = st.columns([1, 1, 1])
with col1:
    consulta = st.text_input("Ingrese el número de identificación del **paciente**")
with col2:
    st.write("")  # Espacio en blanco
    st.write("")  # Más espacio para empujar el botón hacia abajo
    ejecutar_consulta = st.button("🔍 Consultar")

if consulta and (ejecutar_consulta or not st.session_state.consulta_realizada):
    if consulta.isdigit():  # Asegura que el ID es un número
        query = "SELECT PERIODO, VOLANTE, TRASLADOS_AUTORIZADOS, DISPONIBLES, COD_AXSEG, MIPRES, COORDINACIÓN FROM mi_tabla WHERE ID = ?"
        df = pd.read_sql_query(query, conn, params=(consulta,))

        query_2 = """
        SELECT
            mi_tabla.NOMBRE,
            mi_tabla.TIPO_ID,
            mi_tabla.PROGRAMA,
            mi_tabla.CIUDAD,
            coordinacion.Link,
            coordinacion.CEL,
            coordinacion.TelCoord
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


            col1, col2 = st.columns([2, 1])
            with col1:
                st.subheader(f"👤{tipo}-{consulta} | {nombre} | {ciudad}")
                        
            with col2:
                periodos_unicos = df["PERIODO"].unique()
                selected_periodo = st.selectbox("Selecciona el periodo para filtrar:", options=["Todos"] + list(periodos_unicos))
        
            if selected_periodo != "Todos":
                df_filtrado = df[df["PERIODO"] == selected_periodo]
            else:
                df_filtrado = df  # Mostrar todos los datos si no hay filtro
            
            st.data_editor(df_filtrado, use_container_width=True, hide_index=True, disabled=True)
            st.markdown("💡**Muy bien hemos encontrado autorizaciones, si tienes traslados disponibles puedes solicitar tus servicios.**")
            
            tel_at = df_2["CEL"].values[0]
            mensaje = "Hola atencion quiero más información."
            mensaje_codificado = urllib.parse.quote(mensaje)  # Codifica caracteres especiales
            url_whatsapp_at = f"https://wa.me/{tel_at}?text={mensaje_codificado}"
            
            tel_co = df_2["TelCoord"].values[0]
            mensaje = "Hola Coord quiero más información."
            mensaje_codificado = urllib.parse.quote(mensaje)  # Codifica caracteres especiales
            url_whatsapp_co = f"https://wa.me/{tel_co}?text={mensaje_codificado}"
            
            col1, col2, col3 = st.columns([1, 1, 1])
            col1.link_button("📅 Solicitar Servicios",link, use_container_width=True)  # Izquierda
            col2.link_button("🗣️​ Atención Paciente vía WhatsApp", url_whatsapp_at, use_container_width=True)  # Centro
            col3.link_button("✏️ Cancelar/modificar un servicio vía WhatsApp", url_whatsapp_co, use_container_width=True)  # Derecha


    else:
        st.error("Por favor, ingrese un ID numérico válido.")
conn.close()
