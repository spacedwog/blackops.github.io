import streamlit as st
import hashlib
import socket

def exibir_interface(bb):
    st.subheader("Segurança e Análise")
    ip = socket.gethostbyname(socket.gethostname())
    st.write(f"IP local: `{ip}`")
    
    texto = st.text_input("Texto para hash:")
    if texto:
        hash_md5 = hashlib.md5(texto.encode()).hexdigest()
        st.code(f"MD5: {hash_md5}")
        bb.set("hash", hash_md5)