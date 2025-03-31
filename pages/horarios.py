import streamlit as st

col1,col2 = st.columns([1,8])
with col1:
    st.image("Imagen1.png", width=150)  
with col2:
    st.write("")  # Espacio en blanco
    st.title("Pagina 2 perra")

