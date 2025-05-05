import os
import joblib
import pickle
import shutil
import streamlit as st
from datetime import datetime

class GerenciadorModelo:

    def __init__(self, log_path="log.txt"):
        self.log_path = log_path

    def log_evento(self, mensagem):
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        with open(self.log_path, "a") as log_file:
            log_file.write(f"[{timestamp}] {mensagem}\n")

    def salvar_arquivo(self, modelo, diretorio, nome_arquivo):
        if st.button("💾 Salvar modelo localmente"):
            try:
                os.makedirs(diretorio, exist_ok=True)
                caminho_completo = os.path.join(diretorio, nome_arquivo)

                # Backup automático
                if os.path.exists(caminho_completo):
                    caminho_backup = caminho_completo + ".bak"
                    shutil.copy2(caminho_completo, caminho_backup)
                    self.log_evento(f"Backup criado: {caminho_backup}")
                    st.info("📦 Backup do modelo anterior criado.")

                # Salvar modelo
                joblib.dump(modelo, caminho_completo)
                st.success(f"✅ Modelo salvo com sucesso em: {caminho_completo}")
                self.log_evento(f"Modelo salvo: {caminho_completo}")
                return caminho_completo
            except Exception as e:
                st.error(f"❌ Erro ao salvar o modelo: {e}")
                self.log_evento(f"Erro ao salvar modelo: {e}")
                return None

    def carregar_arquivo(self, diretorio, nome_arquivo):
        caminho = os.path.join(diretorio, nome_arquivo)

        if not os.path.exists(caminho):
            st.error("❌ Arquivo não encontrado.")
            self.log_evento(f"Erro: Arquivo não encontrado - {caminho}")
            return None

        if st.button("📂 Carregar modelo salvo"):
            try:
                modelo_carregado = joblib.load(caminho)
                st.success("✅ Modelo carregado com sucesso via joblib!")
                self.log_evento(f"Modelo carregado com joblib: {caminho}")
            except Exception as e_joblib:
                st.warning("⚠️ Falha com joblib. Tentando com pickle...")

                try:
                    with open(caminho, 'rb') as f:
                        modelo_carregado = pickle.load(f)
                    st.success("✅ Modelo carregado com sucesso via pickle!")
                    self.log_evento(f"Modelo carregado com pickle: {caminho}")
                except Exception as e_pickle:
                    st.error("❌ Falha com joblib e pickle. O arquivo está corrompido.")
                    st.error(f"Erro: {e_pickle}")
                    self.log_evento(f"Arquivo corrompido: {caminho} | Erro: {e_pickle}")
                    try:
                        os.remove(caminho)
                        st.warning("🚮 Arquivo corrompido foi removido.")
                        self.log_evento(f"Arquivo removido: {caminho}")
                    except Exception as e_remover:
                        st.error(f"❌ Falha ao remover o arquivo: {e_remover}")
                        self.log_evento(f"Erro ao remover arquivo: {e_remover}")
                    return None

            try:
                st.write("Exemplo de predição com entrada [5.1, 3.5, 1.4, 0.2]:")
                pred = modelo_carregado.predict([[5.1, 3.5, 1.4, 0.2]])
                st.write(f"🔮 Predição: {pred}")
            except Exception as e_pred:
                st.error(f"❌ Erro ao realizar predição: {e_pred}")
                self.log_evento(f"Erro de predição: {e_pred}")

            return modelo_carregado