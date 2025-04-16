# -----------------------------
# consciencia/dns_streamlit_app.py
# -----------------------------
import streamlit as st
from datetime import datetime
from consultar_dns import DataScienceDNS

dns_tool = DataScienceDNS()

st.set_page_config(page_title="Análise DNS", layout="wide")

st.title("🧠 Monitoramento DNS com Data Science")

# Entrada manual
dominio = st.text_input("🌐 Digite o domínio a consultar", "google.com")
if st.button("Consultar Agora"):
    resultado = dns_tool.consultar_dns(dominio, datetime.now())
    st.success(f"Consulta realizada para {dominio}")
    st.json(resultado)

# Agendamento
if st.checkbox("⏱️ Agendar coletas automáticas"):
    intervalo = st.slider("Intervalo (segundos)", 5, 60, 10)
    if st.button("Iniciar Agendamento"):
        dns_tool.agendar_coleta(dominio, intervalo)
        st.info(f"Coleta automática iniciada para {dominio} a cada {intervalo} segundos.")

# Dados em tempo real
if not dns_tool.dns_data.empty:
    st.subheader("📊 Dados Coletados")
    st.dataframe(dns_tool.dns_data)

    # Exportação
    col1, col2 = st.columns(2)
    with col1:
        if st.button("💾 Exportar para CSV"):
            dns_tool.exportar_csv()
            st.success("Exportado como dados_dns.csv")

    with col2:
        if st.button("📤 Exportar para MongoDB"):
            dns_tool.exportar_mongodb()
            st.success("Dados enviados ao MongoDB!")

    # Gráficos
    st.subheader("📈 Gráficos Interativos")
    dns_tool.visualizar_metricas()