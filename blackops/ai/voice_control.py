# -----------------------------
# ai/voice_control.py
# -----------------------------
import pandas as pd
import soundfile as sf
from io import BytesIO
import streamlit as st
import sounddevice as sd
from datetime import datetime
import speech_recognition as sr

import firebase_admin
from github import Github
from transformers import pipeline
from deep_translator import GoogleTranslator
from firebase_admin import credentials, firestore

import socket

import os
import re
from gtts import gTTS
from ai.consciencia.consultar_dns import DataScienceDNS

class VoiceGitHubAssistant:
    def __init__(self, github_token, mongo_uri, repo_name="openai/whisper"):
        self.github = Github(github_token)
        self.repo = self.github.get_repo(repo_name)
        self.repo_name = repo_name
        self.summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

        cred = credentials.Certificate(os.path.exists("blackops/security/firebase_key.json"))
        if not firebase_admin._apps:
            firebase_admin.initialize_app(cred)

        self.db = firestore.client()
        self.logs = self.db.collection("logs")


        # Inicializa um DataFrame para armazenar consultas DNS
        self.dns_consultas = pd.DataFrame(columns=["timestamp", "dominio", "ip", "status"])

        # Instancia a classe de Data Science DNS
        self.dns_data_science = DataScienceDNS()

    # Método para consulta DNS aprimorado com análise de Data Science
    def consultar_dns(self, dominio):
        try:
            # Realiza uma consulta DNS para obter o IP do domínio
            ip = socket.gethostbyname(dominio)
            status = "sucesso"

            # Adiciona a consulta ao DataFrame para análise futura
            nova_consulta = {
                "timestamp": pd.Timestamp.now(),
                "dominio": dominio,
                "ip": ip,
                "status": status
            }

            # Converta o dicionário para um DataFrame
            nova_consulta_df = pd.DataFrame([nova_consulta])

            # Agora concatene com o DataFrame existente
            self.dns_consultas = pd.concat([self.dns_consultas, nova_consulta_df], ignore_index=True)

            # Realiza uma análise simples sobre os resultados de DNS
            analise = self.analisar_dns(dominio, ip)

            # Chamando a análise de Data Science para DNS
            self.dns_data_science.consultar_dns(dominio, pd.Timestamp.now())

            return f"O IP do domínio {dominio} é: {ip}. {analise}"

        except socket.gaierror as e:
            status = "erro"
            # Adiciona o erro ao DataFrame
            nova_consulta = {
                "timestamp": pd.Timestamp.now(),
                "dominio": dominio,
                "ip": None,
                "status": status
            }
            self.dns_consultas = pd.concat(
                [self.dns_consultas, pd.DataFrame([nova_consulta])],
                ignore_index=True
            )

            return f"Erro ao consultar o DNS: {str(e)}"

    # Método de análise simples para DNS
    def analisar_dns(self, dominio, ip):
        # Análise simples: verifica se o IP retornado é um IP válido ou se houve erro
        if ip:
            return f"A consulta ao domínio {dominio} foi bem-sucedida e o IP retornado foi {ip}."
        else:
            return f"A consulta ao domínio {dominio} falhou. Nenhum IP foi retornado."

    # Método para exibir estatísticas sobre as consultas DNS
    def exibir_estatisticas_dns(self):
        # Exibe as estatísticas das consultas DNS realizadas até o momento
        total_consultas = len(self.dns_consultas)
        consultas_sucesso = len(self.dns_consultas[self.dns_consultas["status"] == "sucesso"])
        consultas_erro = len(self.dns_consultas[self.dns_consultas["status"] == "erro"])

        # Exibe as consultas feitas
        st.write(f"Total de consultas DNS realizadas: {total_consultas}")
        st.write(f"Consultas bem-sucedidas: {consultas_sucesso}")
        st.write(f"Consultas com erro: {consultas_erro}")

        # Exibe um gráfico de barras das estatísticas
        st.bar_chart({
            "Sucesso": consultas_sucesso,
            "Erro": consultas_erro
        })

    def gravar_audio(self, duracao=5, arquivo_saida='voz_usuario.wav', samplerate=44100):
        st.write("🎙️ Gravando sua voz...")

        audio = sd.rec(int(duracao * samplerate), samplerate=samplerate, channels=1, dtype='int16')
        sd.wait()
        sf.write(arquivo_saida, audio, samplerate)
        st.success(f"✅ Áudio gravado: {arquivo_saida}")
        return arquivo_saida

    def reproduzir_audio(self, arquivo='voz_usuario.wav'):
        st.audio(arquivo, format='audio/wav')

    def speak(self, text):
        # Mostra na interface o que será falado
        with st.chat_message("assistant"):
            st.markdown(f"**🧠 Consciência Virtual diz:**\n{text}")

        # Converte texto em fala
        tts = gTTS(text=text, lang='pt-br')
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)

        # Reproduz o áudio diretamente no navegador
        st.audio(audio_bytes, format='audio/mp3')

    def traduzir(self, texto, origem='en'):
        try:
            return GoogleTranslator(source=origem, target='pt').translate(texto)
        except Exception as e:
            return f"[Erro na tradução] {str(e)}"
        
    def normalizar_comando(self, comando):
        comando = comando.lower().strip()

        # Correções de termos comuns mal interpretados por voz
        mapeamento = {

            "consultar dns": "consultar dns", "consultar dsn": "consultar dns",
            
            "comando recente": "buscar logs", "estrelas repositório": "estrelas",

            "último commit": "último commit", "último commit": "último commit",

            "comite": "commit", "commite": "commit", "compromisso": "commit",

            "comprometimento": "commit", "comprometimento": "commit", "comite": "commit",

            "commit": "commit", "repositório": "repositório", "repositorio": "repositório",

            "histórico de usuário": "buscar logs", "histórico de data": "buscar logs",

            "resumo do repositório": "resumo", "repositorio": "repositório", "repo": "repositório",

            "requisição de puxar": "pull request", "pau request": "pull request", "pull": "pull request",

            "problemas abertos": "issues", "linguagem": "linguagem principal", "linguagem principal": "linguagem principal",

            "quem criou": "criador", "quantas estrelas": "estrelas", "quantos estrelas": "estrelas",

            "resumo inteligente": "augment", "aumentar": "augment", "aumentar repositório": "augment",

            "buscar logs": "buscar logs", "mostrar histórico": "buscar logs", "histórico de comandos": "buscar logs",

            "estatísticas de voz": "estatísticas de voz", "histórico de repositório": "buscar logs",

            "repositório": "repositório", "repositorio": "repositório", "repo": "repositório",
            "repositório": "repositório", "repositorio": "repositório", "repo": "repositório",

            "quantos acertos": "estatísticas de voz", "quantas acertos": "estatísticas de voz",
            "quantas falhas": "estatísticas de voz", "estatísticas de voz": "estatísticas de voz",

            "última atualização": "último commit", "último commit": "último commit",

            "últimos históricos de data": "buscar logs", "comandos recentes": "buscar logs",

            "últimos históricos de data": "buscar logs", "últimos históricos de comandos": "buscar logs",

            "últimos históricos de usuário": "buscar logs", "últimos históricos de repositório": "buscar logs",

            "histórico de voz": "buscar logs", "últimos logs": "buscar logs", "últimos históricos": "buscar logs",

            "últimos históricos de voz": "buscar logs", "últimos históricos de comandos": "buscar logs",
            "últimos históricos de voz": "buscar logs", "últimos históricos de repositório": "buscar logs",
            
            "últimos históricos de comandos": "buscar logs", "últimos históricos de voz": "buscar logs",
            "últimos históricos de comandos": "buscar logs", "últimos históricos de voz": "buscar logs",

            "últimos históricos de repositório": "buscar logs", "últimos históricos de usuário": "buscar logs",
            "últimos históricos de repositório": "buscar logs", "últimos históricos de usuário": "buscar logs",
            "últimos históricos de repositório": "buscar logs", "últimos históricos de usuário": "buscar logs",
        }

        for errado, certo in mapeamento.items():
            if errado in comando:
                comando = comando.replace(errado, certo)

        filtros = {}

        # Extração de data
        match_data = re.search(r"(desde|de) (\d{1,2}) de (\w+)", comando)
        if match_data:
            dia, mes = match_data.groups()[1], match_data.groups()[2]
            meses = {
                "janeiro": 1, "fevereiro": 2, "março": 3, "abril": 4,
                "maio": 5, "junho": 6, "julho": 7, "agosto": 8,
                "setembro": 9, "outubro": 10, "novembro": 11, "dezembro": 12
            }
            mes_num = meses.get(mes)
            if mes_num:
                filtros['data'] = datetime(datetime.now().year, mes_num, int(dia))

        # Detecção de repositório (ex: "repositório flask-restful")
        match_repo = re.search(r"repositório ([\w\-]+)", comando)
        if match_repo:
            filtros['repositorio'] = match_repo.group(1)

        # Detecção de usuário GitHub (ex: "usuário torvalds")
        match_user = re.search(r"usuário (\w+)", comando)
        if match_user:
            filtros['usuario'] = match_user.group(1)

        # Detecção de termos adicionais como commits, estrelas e issues
        if "último commit" in comando:
            comando = comando.replace("último commit", "commit")

        if "estrelas" in comando:
            comando = comando.replace("estrelas", "quantas estrelas")

        return comando, filtros

    def ask_github_ai(self, question):
        try:
            # Proteção extra
            if isinstance(question, tuple):
                question, _ = question

            comando, filtros = self.normalizar_comando(question)

            # Verifica se o comando é para consultar DNS
            if "consultar dns" in comando:
                dominio = question.split("consultar dns")[-1].strip()  # Pega o domínio após o comando
                resposta_dns = self.consultar_dns(dominio)  # Executa a consulta DNS
                self.salvar_log(question, comando, resposta_dns)  # Salva o log da consulta DNS
                return resposta_dns
            
            elif "estatísticas de voz" in comando:
                estatisticas = self.contar_acertos_erros()
                return f"Total de interações: {estatisticas['total']}, Acertos: {estatisticas['acertos']}, Erros: {estatisticas['erros']}, Precisão: {estatisticas['precisao']}%."

            elif "buscar logs" in comando:
                return self.buscar_logs_mongodb(filtros)

            elif "commit" in comando:
                commit = self.repo.get_commits()[0]
                return self.traduzir(f"O último commit foi de {commit.commit.author.name}: {commit.commit.message}")

            elif "resumo" in question:
                readme = self.repo.get_readme().decoded_content.decode()
                summary = self.summarizer(readme[:1024], max_length=60, min_length=30, do_sample=False)
                return self.traduzir(summary[0]['summary_text'])

            elif "linguagem principal" in question:
                return f"A linguagem principal do repositório é {self.repo.language}."

            elif "estrelas" in question:
                return f"O repositório possui {self.repo.stargazers_count} estrelas."

            elif "issues" in question:
                return f"O número de issues abertas é {self.repo.open_issues_count}."

            elif "criador" in question:
                return f"O criador do repositório é {self.repo.owner.login}."

            elif "augment" in question:
                return self.augment_repo()

            else:
                return "Não entendi a pergunta sobre o GitHub."

        except Exception as e:
            return f"[Erro no GitHub] {str(e)}"

    def salvar_log(self, comando_original, comando_normalizado, resposta, erro=None):

        self.logs.add({
            "timestamp": datetime.now(),
            "repo": self.repo_name,
            "comando_original": comando_original,
            "comando_normalizado": comando_normalizado,
            "resposta": resposta,
            "erro": erro
        })

    def contar_acertos_erros(self):
        total = self.logs.count_documents({})
        erros = self.logs.count_documents({"erro": {"$ne": None}})
        acertos = total - erros

        return {
            "total": total,
            "acertos": acertos,
            "erros": erros,
            "precisao": round((acertos / total) * 100, 2) if total > 0 else 0
        }

    def executar_voz(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("Fale algo relacionado ao GitHub ou pergunte quantos acertos e erros você teve.")
            audio = recognizer.listen(source)
            try:
        
                with st.spinner("🎙 Gravando sua pergunta..."):
                    caminho_audio = self.gravar_audio()

                self.reproduzir_audio(caminho_audio)

                comando = recognizer.recognize_google(audio, language="pt-BR")

                comando_lower = comando.lower().strip()

                # 👀 Verifica se é uma consulta de DNS
                if "consultar dns" in comando_lower:
                    dominio = comando_lower.split("consultar dns")[-1].strip()
                    resposta_dns = self.consultar_dns(dominio)
                    self.speak(resposta_dns)
                    return resposta_dns

                # 👇 Fluxo normal de comando GitHub
                comando_normalizado, filtros = self.normalizar_comando(comando)
                resposta = self.ask_github_ai(comando)

                self.salvar_log(comando, comando_normalizado, resposta)
                self.speak(resposta)
                
            
                with open("log_interacoes.txt", "a") as log:
                    log.write(f"Usuário: {self.github.get_user}\nAssistente: {resposta}\n\n")

                return f"Você disse: {comando}\nGitHub respondeu: {resposta}"

            except sr.UnknownValueError:
                erro = "Não entendi o que você disse."
                self.salvar_log(None, None, None, erro)
                self.speak(erro)
                return erro

            except sr.RequestError:
                erro = "Erro na API de reconhecimento."
                self.salvar_log(None, None, None, erro)
                self.speak(erro)
                return erro

    def interagir_por_voz(self):
        recognizer = sr.Recognizer()

        st.write("🎤 Pressione para gravar sua pergunta de voz ao GitHub Assistant.")
        if st.button("🎧 Falar com o Assistente"):
        
            with st.spinner("🎙 Gravando sua pergunta..."):
                arquivo_audio = self.gravar_audio()

            with sr.AudioFile(arquivo_audio) as source:
                st.write("🎧 Processando sua voz...")
                audio = recognizer.record(source)

                try:
                    texto = recognizer.recognize_google(audio, language='pt-BR')
                    st.success(f"📜 Texto reconhecido: *{texto}*")
                    
                    resposta = self.ask_github_ai(texto)
                    self.speak(resposta)

                except sr.UnknownValueError:
                    st.error("❌ Não foi possível entender o áudio.")
                except sr.RequestError as e:
                    st.error(f"❌ Erro ao acessar o serviço de reconhecimento: {e}")
