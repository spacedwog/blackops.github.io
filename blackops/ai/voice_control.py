# -----------------------------
# ai/voice_assistant.py
# -----------------------------
import pandas as pd
import soundfile as sf
from io import BytesIO
import streamlit as st
import sounddevice as sd
from datetime import datetime
import speech_recognition as sr

import socket
import re
from gtts import gTTS
from deep_translator import GoogleTranslator

class VoiceAssistant:
    def __init__(self):
        self.dns_consultas = pd.DataFrame(columns=["timestamp", "dominio", "ip", "status"])

    def consultar_dns(self, dominio):
        try:
            ip = socket.gethostbyname(dominio)
            status = "sucesso"

            nova_consulta = {
                "timestamp": pd.Timestamp.now(),
                "dominio": dominio,
                "ip": ip,
                "status": status
            }
            self.dns_consultas = pd.concat([self.dns_consultas, pd.DataFrame([nova_consulta])], ignore_index=True)

            return f"O IP do domínio {dominio} é: {ip}."
        except socket.gaierror as e:
            status = "erro"
            nova_consulta = {
                "timestamp": pd.Timestamp.now(),
                "dominio": dominio,
                "ip": None,
                "status": status
            }
            self.dns_consultas = pd.concat([self.dns_consultas, pd.DataFrame([nova_consulta])], ignore_index=True)
            return f"Erro ao consultar o DNS: {str(e)}"

    def exibir_estatisticas_dns(self):
        total_consultas = len(self.dns_consultas)
        consultas_sucesso = len(self.dns_consultas[self.dns_consultas["status"] == "sucesso"])
        consultas_erro = len(self.dns_consultas[self.dns_consultas["status"] == "erro"])

        st.write(f"Total de consultas DNS realizadas: {total_consultas}")
        st.write(f"Consultas bem-sucedidas: {consultas_sucesso}")
        st.write(f"Consultas com erro: {consultas_erro}")

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
        with st.chat_message("assistant"):
            st.markdown(f"**🧠 Assistente diz:**\n{text}")

        tts = gTTS(text=text, lang='pt-br')
        audio_bytes = BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        st.audio(audio_bytes, format='audio/mp3')

    def traduzir(self, texto, origem='en'):
        try:
            return GoogleTranslator(source=origem, target='pt').translate(texto)
        except Exception as e:
            return f"[Erro na tradução] {str(e)}"

    def executar_voz(self):
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            self.speak("Fale algo como 'consultar DNS google.com'")
            audio = recognizer.listen(source)
            try:
                with st.spinner("🎙 Gravando sua pergunta..."):
                    caminho_audio = self.gravar_audio()

                self.reproduzir_audio(caminho_audio)

                comando = recognizer.recognize_google(audio, language="pt-BR")
                comando_lower = comando.lower().strip()

                if "consultar dns" in comando_lower:
                    dominio = comando_lower.split("consultar dns")[-1].strip()
                    resposta_dns = self.consultar_dns(dominio)
                    self.speak(resposta_dns)
                    return resposta_dns
                else:
                    resposta = "Comando não reconhecido. Diga algo como 'consultar DNS google.com'."
                    self.speak(resposta)
                    return resposta

            except sr.UnknownValueError:
                erro = "Não entendi o que você disse."
                self.speak(erro)
                return erro

            except sr.RequestError:
                erro = "Erro na API de reconhecimento."
                self.speak(erro)
                return erro

    def interagir_por_voz(self):
        recognizer = sr.Recognizer()

        st.write("🎤 Pressione para gravar sua pergunta.")
        if st.button("🎧 Falar com o Assistente"):
            with st.spinner("🎙 Gravando sua pergunta..."):
                arquivo_audio = self.gravar_audio()

            with sr.AudioFile(arquivo_audio) as source:
                st.write("🎧 Processando sua voz...")
                audio = recognizer.record(source)

                try:
                    texto = recognizer.recognize_google(audio, language='pt-BR')
                    st.success(f"📜 Texto reconhecido: *{texto}*")

                    if "consultar dns" in texto.lower():
                        dominio = texto.lower().split("consultar dns")[-1].strip()
                        resposta = self.consultar_dns(dominio)
                        self.speak(resposta)
                    else:
                        self.speak("Comando não reconhecido.")

                except sr.UnknownValueError:
                    st.error("❌ Não foi possível entender o áudio.")
                except sr.RequestError as e:
                    st.error(f"❌ Erro ao acessar o serviço de reconhecimento: {e}")