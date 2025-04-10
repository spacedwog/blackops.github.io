import time
import serial
import binascii
import streamlit as st

# Simulação do módulo BlackOps
class BlackOps:
    def __init__(self, porta='/dev/ttyUSB0', baud=9600):
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

        tab1, tab2, tab3 = st.tabs(["🔐 Relay/Firewall", "🔎 Análise XOR", "🛠️ Comandos Táticos"])

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

        st.divider()
        if st.button("🔙 Voltar para tela principal"):
            st.session_state["modo"] = "inicio"
            st.rerun()

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
            st.experimental_rerun()

    elif st.session_state["modo"] == "blackops":
        ops = BlackOps()
        ops.exibir_blackops()

# Execução principal
if __name__ == "__main__":
    main()