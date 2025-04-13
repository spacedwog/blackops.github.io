import time
import serial
import binascii
import numpy as np
import streamlit as st
from scipy.constants import epsilon_0

# Simulação do módulo BlackOps
class BlackOps:
    def __init__(self, porta='COM4', baud=9600):
        try:
            self.ser = serial.Serial(porta, baud, timeout=1)
        except:
            self.ser = None

    def enviar_comando(self, comando):
        if self.ser:
            self.ser.write(comando.encode())
            time.sleep(1)
            return self.ser.read_all().decode(errors='ignore')
        return "Serial não disponível"

    def relay_on(self):
        return self.enviar_comando("RELAY_ON")

    def relay_off(self):
        return self.enviar_comando("RELAY_OFF")

    def analisar_xor(self, data, key):
        result = ''.join([chr(ord(c) ^ ord(key)) for c in data])
        return result

    def exibir_blackops(self):
        st.title("🕶️ Painel BlackOps - Cibersegurança Interativa")
        st.subheader("🔐 Acesso restrito")

        tab1, tab2, tab3, tab4 = st.tabs(["🔐 Relay/Firewall", "🔎 Análise XOR", "🛠️ Comandos Táticos", "⚛️ Lilith AI"])

        with tab1:
            st.subheader("Controle de Relay / Firewall")
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔌 Ativar Relay"):
                    resposta = self.relay_on()
                    st.success(f"Resposta: {resposta}")
            with col2:
                if st.button("❌ Desativar Relay"):
                    resposta = self.relay_off()
                    st.warning(f"Resposta: {resposta}")

        with tab2:
            st.subheader("Decodificação com XOR")
            dado = st.text_input("Digite a string codificada")
            chave = st.text_input("Digite a chave XOR", max_chars=1)
            if st.button("Analisar"):
                if dado and chave:
                    resultado = self.analisar_xor(dado, chave)
                    st.code(resultado, language='text')
                else:
                    st.error("Preencha ambos os campos.")

        with tab3:
            st.subheader("Terminal Serial - Comando Tático")
            comando = st.text_input("Comando direto ao hardware")
            if st.button("Executar Comando"):
                output = self.enviar_comando(comando)
                st.text_area("Resposta Serial", output, height=150)
                
        with tab4:
            st.subheader("Lilith AI")
            q1 = st.number_input("Carga 1 (C)", value=1e-9, format="%.2e")
            q2 = st.number_input("Carga 2 (C)", value=1e-9, format="%.2e")
            r = st.number_input("Distância (m)", value=0.05)

            if st.button("Calcular Força"):
                F = self.calcular_forca_eletrica(q1, q2, r)
                st.success(f"Força Elétrica: {F:.2e} N")

            st.image("imagem/esfera_eletrica_azul.png", caption="Esfera Elétrica Azul", use_container_width=True)


        st.divider()
        if st.button("🔙 Voltar para tela principal"):
            st.session_state["modo"] = "inicio"
            st.rerun()

    def calcular_forca_eletrica(self, q1: float, q2: float, r: float) -> float:
        """
        Calcula a força elétrica entre duas cargas pontuais usando a Lei de Coulomb.

        Parâmetros:
        q1 (float): carga 1 em Coulombs
        q2 (float): carga 2 em Coulombs
        r (float): distância entre as cargas em metros

        Retorna:
        float: força elétrica em Newtons (N)
        """
        if r == 0:
            raise ValueError("A distância entre as cargas não pode ser zero.")
        k = 1 / (4 * np.pi * epsilon_0)
        F = k * q1 * q2 / r**2
        return F

# Gerenciador de navegação entre páginas
def main():
    st.set_page_config(page_title="BlackOps Dashboard", layout="wide")

    if "modo" not in st.session_state:
        st.session_state["modo"] = "inicio"

    if st.session_state["modo"] == "inicio":
        st.title("🌐 Dashboard Principal")
        st.write("Clique abaixo para ativar o painel BlackOps.")
        if st.button("🚨 Ativar BlackOps"):
            st.session_state["modo"] = "blackops"
            st.rerun()

    elif st.session_state["modo"] == "blackops":
        ops = BlackOps()
        ops.exibir_blackops()

# Execução principal
if __name__ == "__main__":
    main()