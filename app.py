import streamlit as st
import json
from oauth import get_google_auth_url, get_tokens, get_user_info
from blackboard import blackboard
from database import db
from nodemcu import enviar_para_esp8266

# Carrega config
with open("config.json") as f:
    config = json.load(f)

st.set_page_config(page_title="CyberDS Login", layout="centered")

st.title("🔐 Login com Google - Cibersegurança + DataScience")

query_params = st.query_params()
code = query_params.get("code", [None])[0]

if "user" not in st.session_state:
    st.session_state.user = None

if code and not st.session_state.user:
    tokens = get_tokens(code, config)
    user = get_user_info(tokens["access_token"])
    st.session_state.user = user
    db.upsert_user(user)
    blackboard.set(user["id"], "status", "autenticado")

if not st.session_state.user:
    auth_url = get_google_auth_url(config)
    st.markdown(f"[Login com Google]({auth_url})")
else:
    user = st.session_state.user
    st.image(user["picture"], width=100)
    st.write(f"Bem-vindo, {user['name']} ({user['email']})")

    st.subheader("📊 Análise e Interação")
    if st.button("Enviar alerta para NodeMCU"):
        resposta = enviar_para_esp8266("alert", {"user": user["id"], "evento": "login"})
        st.write("Resposta ESP:", resposta)

    st.subheader("📁 Seus Dados")
    data = db.get_user(user["id"])
    st.json({
        "ID": data[0],
        "Email": data[1],
        "Nome": data[2],
        "Foto": data[3],
        "Status Blackboard": blackboard.get(user["id"], "status")
    })