import streamlit as st

# ===== Estilo CSS para bordas e design tecnológico =====
st.markdown("""
    <style>
        .main {
            background-color: #0f1117;
            padding: 2rem;
            border-radius: 15px;
            border: 3px solid #1f2c56;
            box-shadow: 0 0 30px rgba(0, 255, 255, 0.2);
        }
        .sidebar .sidebar-content {
            background-color: #1a1a2e;
        }
        h1, h2, h3, p {
            color: #00f5d4;
        }
        .stButton>button {
            background-color: #0d7377;
            color: white;
            border-radius: 8px;
        }
    </style>
""", unsafe_allow_html=True)

# ===== Título principal do painel =====
st.title("🔧 Painel Tecnológico Interativo")

# ===== Menu lateral com navegação =====
menu = st.sidebar.radio("Menu", ["Dashboard", "Configurações", "Sobre"])

# ===== Conteúdo baseado na seleção do menu =====
if menu == "Dashboard":
    st.subheader("📊 Visualização de Dados")
    st.line_chart({"CPU": [10, 20, 30, 25, 40], "Memória": [15, 25, 20, 30, 35]})
    st.success("Dados atualizados com sucesso!")

elif menu == "Configurações":
    st.subheader("⚙️ Ajustes do Sistema")
    modo = st.selectbox("Escolha o modo", ["Automático", "Manual", "Diagnóstico"])
    nivel = st.slider("Nível de operação", 1, 10, 5)
    st.write(f"Modo: {modo}, Nível: {nivel}")

elif menu == "Sobre":
    st.subheader("ℹ️ Informações do Sistema")
    st.markdown("""
        **Projeto:** Painel Tecnológico  
        **Versão:** 1.0  
        **Desenvolvido com:** Streamlit  
        **Execução:** Compatível com PowerShell
    """)

# Rodapé
st.markdown("<hr style='border:1px solid #00f5d4;'>", unsafe_allow_html=True)
st.caption("Desenvolvido por você — Streamlit Power Panel 💡")