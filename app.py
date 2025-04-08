# app.py
import json
import streamlit as st
from blackboard import blackboard
from nodemcu import enviar_para_esp8266
from database import create_or_update_user, get_user
from oauth import get_google_auth_url, get_tokens, get_user_info

with open("config.json") as f:
    config = json.load(f)

st.set_page_config(page_title="CyberDS Login", layout="centered")
st.title("🔐 Login com Google - Cibersegurança + DataScience")

query_params = st.query_params
code = query_params.get("code", [None])[0]
st.write(f"🔑 Código recebido: {code}")

if "user" not in st.session_state:
    st.session_state.user = None

if code and not st.session_state.user:
    tokens = get_tokens(code, config)
    access_token = tokens.get("access_token")

    if access_token:
        user = get_user_info(access_token)
        st.session_state.user = user
        create_or_update_user(user)
        st.experimental_set_query_params()  # limpa a URL
        st.success(f"Bem-vindo, {user['name']} ({user['email']})")
    else:
        st.error("Falha ao obter token de acesso. Verifique o console para mais detalhes.")

if not st.session_state.user:
    auth_url = get_google_auth_url(config)
    st.link_button("🔑 Login com Google", url=auth_url)
else:
    user = st.session_state.user
    st.image(user["picture"], width=100)
    st.write(f"Bem-vindo, {user['name']} ({user['email']})")

    st.subheader("📊 Análise e Interação")
    if st.button("Enviar alerta para NodeMCU"):
        resposta = enviar_para_esp8266("alert", {"user": user["id"], "evento": "login"})
        st.write("Resposta ESP:", resposta)

    st.subheader("📁 Seus Dados")
    data = get_user(user["id"])
    st.json({
        "ID": data[0],
        "Email": data[1],
        "Nome": data[2],
        "Foto": data[3],
        "Status Blackboard": blackboard.get(user["id"], "status")
    })