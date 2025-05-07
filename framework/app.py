# sourcery skip: remove-redundant-fstring
import streamlit as st
from firewall import Firewall, FirewallRule

st.set_page_config(page_title="Firewall Interface", layout="wide")

fw = Firewall()

st.title("🔐 Firewall Interface com Streamlit")

tab1, tab2, tab3 = st.tabs(["📜 Regras", "📦 Simular Pacote", "📁 Exportar/Importar"])

with tab1:
    st.subheader("Regras Atuais")
    for i, rule in enumerate(fw.rules):
        st.write(f"{i+1}. {rule.to_dict()}")
        if st.button(f"Remover Regra {i+1}", key=f"remove_{i}"):
            fw.remove_rule(i)
            st.experimental_user()

    st.divider()
    st.subheader("Adicionar Nova Regra")
    src = st.text_input("IP de Origem (ex: 192.168.1.1 ou *)", key="src")
    dst = st.text_input("IP de Destino (ex: 10.0.0.1 ou *)", key="dst")
    port = st.text_input("Porta (ex: 80 ou *)", key="port")
    action = st.selectbox("Ação", ["allow", "deny"], key="action")

    if st.button("Adicionar Regra"):
        new_rule = FirewallRule(src, dst, port, action)
        fw.add_rule(new_rule)
        st.success("Regra adicionada com sucesso!")
        st.experimental_user()

with tab2:
    st.subheader("Simular Verificação de Pacote")
    test_src = st.text_input("IP Origem do Pacote", key="test_src")
    test_dst = st.text_input("IP Destino do Pacote", key="test_dst")
    test_port = st.text_input("Porta", key="test_port")

    if st.button("Verificar"):
        result = fw.check_packet(test_src, test_dst, test_port)
        if result == "allow":
            st.success(f"✔️ Pacote PERMITIDO")
        else:
            st.error(f"⛔ Pacote BLOQUEADO")

with tab3:
    st.subheader("Exportar / Importar Regras")
    if st.button("Exportar para JSON"):
        with open(fw.rules_file, "r") as f:
            st.download_button("📥 Baixar Regras", f.read(), file_name="firewall_rules.json")

    uploaded = st.file_uploader("Importar Regras JSON")
    if uploaded:
        data = uploaded.read().decode("utf-8")
        with open("rules.json", "w") as f:
            f.write(data)
        st.success("Regras importadas com sucesso!")
        st.experimental_user()