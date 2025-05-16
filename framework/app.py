# -----------------------------
# framework/app.py
# -----------------------------
import streamlit as st
from framework.firewall import Firewall, FirewallRule

class App:
    def __init__(self):
        self.fw = Firewall()

    def render_rules_tab(self):
            st.subheader("Regras Atuais")
            for i, rule in enumerate(self.fw.rules):
                st.write(f"{i+1}. {rule.to_dict()}")
                if st.button(f"🗑️ Remover Regra {i+1}", key=f"remove_{i}"):
                    self.fw.remove_rule(i)
                    st.toast("🗑️ Regra removida com sucesso!")
                    st.rerun()

            if st.button("🧹 Limpar Regras"):
                self.fw.clear_rules()
                st.toast("🧹 Regras limpas com sucesso!")
                st.rerun()

            st.divider()
            st.subheader("Adicionar Nova Regra")
            src = st.text_input("IP de Origem (ex: 192.168.1.1 ou *)", key="src")
            dst = st.text_input("IP de Destino (ex: 10.0.0.1 ou *)", key="dst")
            port = st.text_input("Porta (ex: 80 ou *)", key="port")
            action = st.selectbox("Ação", ["allow", "deny"], key="action")

            if st.button("Adicionar Regra"):
                self.fw.add_whois_rules(src, dst, port, action)
                st.success("📥 Regra adicionada com sucesso!")
                st.toast("📥 Regra adicionada com sucesso!")
                st.rerun()

    def render_packet_simulation_tab(self):
            st.subheader("Simular Verificação de Pacote")
            test_src = st.text_input("IP Origem do Pacote", key="test_src")
            test_dst = st.text_input("IP Destino do Pacote", key="test_dst")
            test_port = st.text_input("Porta", key="test_port")

            if st.button("Verificar"):
                result = self.fw.check_packet(test_src, test_dst, test_port)
                if result == "allow":
                    st.success("✔️ Pacote PERMITIDO")
                else:
                    st.error("⛔ Pacote BLOQUEADO")

    def render_import_export_tab(self):
            st.subheader("Exportar / Importar Regras")
            if st.button("Exportar para JSON"):
                with open(self.fw.rules_file, "r") as f:
                    st.download_button("📥 Baixar Regras", f.read(), file_name="firewall_rules.json")

            uploaded = st.file_uploader("Importar Regras JSON")
            if uploaded:
                data = uploaded.read().decode("utf-8")
                with open("rules.json", "w") as f:
                    f.write(data)
                st.success("📥 Regras importadas com sucesso!")
                st.rerun()