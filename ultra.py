import streamlit as st
import gdown
import pandas as pd
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

# Configurar rutas
EXCEL_PATH = "Base_Pacientes_NAL_BOT.xlsx"
DB_PATH = r"G:/Mi unidad/UNIDAD_YVAN/Base_Pacientes_NAL/Base_Pacientes_NAL_BOT.bd"

file_id ="1sqmGuz-npLggyJAt5V9WkBkg6ZZi8fvJ"
url = f"https://docs.google.com/spreadsheets/d/{file_id}"

if not os.path.exists(EXCEL_PATH):
    st.info("Descargando base de datos...")
    gdown.download(url, EXCEL_PATH, fuzzy=True, quiet=False)
    st.success("Base de datos descargada con éxito.")
   
# Función para cargar el Excel a SQLite si ha cambiado
def actualizar_base_datos():
    if not os.path.exists(DB_PATH) or os.path.getmtime(EXCEL_PATH) > os.path.getmtime(DB_PATH):
        df = pd.read_excel(EXCEL_PATH, engine="    ")
        conn = sqlite3.connect(DB_PATH)
        df.to_sql("mi_tabla", conn, if_exists="replace", index=False)
        conn.close()
        st.success("Base de datos actualizada con éxito.")
        return df
    else:
        st.info("Los datos están actualizados.")
        
actualizar_base_datos()
conn = sqlite3.connect(DB_PATH)
# Entrada para consulta SQL (opcional)

consulta = st.text_input("Ingrese el número de identificación")

if consulta:
    if consulta.isdigit():  # Asegura que el ID es un número
        query = "SELECT PERIODO, VOLANTE, TRASLADOS_AUTORIZADOS, DISPONIBLES, COD_AXSEG, MIPRES, COORDINACIÓN FROM mi_tabla WHERE ID = ?"
        df = pd.read_sql_query(query, conn, params=(consulta,))
        query_2 = "SELECT NOMBRE, TIPO_ID, PROGRAMA, CIUDAD FROM mi_tabla WHERE ID = ?"
        df_2 = pd.read_sql_query(query_2, conn, params=(consulta,))
        if df.empty:
            st.warning("No se encontraron resultados.")
        else:
            nombre = df_2["NOMBRE"].values[0]
            ciudad = df_2["CIUDAD"].values[0]
            tipo = df_2["TIPO_ID"].values[0]
            st.subheader(f"👤{tipo}-{consulta} | {nombre} | {ciudad}")
            st.dataframe(df, use_container_width=True)
    else:
        st.error("Por favor, ingrese un ID numérico válido.")
conn.close()


            # col1, col2, col3 = st.columns([1, 1, 1])
            # col1.markdown(f"👤 Nombre: {nombre}")  # Izquierda
            # col2.markdown(f"📍 Ciudad: {ciudad}")  # Centro
            # col3.markdown(f"🎓 Programa: {programa}")  # Derecha
            
