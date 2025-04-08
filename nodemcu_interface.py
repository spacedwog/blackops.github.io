import streamlit as st
import requests

def controle_esp():
    st.subheader("Controle do NodeMCU")
    url = st.text_input("URL do NodeMCU", value="http://192.168.15.8")
    acao = st.selectbox("Ação", ["Ligar LED", "Desligar LED"])

    if st.button("Enviar"):
        comando = "/led/on" if acao == "Ligar LED" else "/led/off"
        try:
            r = requests.get(url + comando)
            st.success(f"Resposta: {r.text}")
        except Exception as e:
            st.error(f"Erro: {e}")