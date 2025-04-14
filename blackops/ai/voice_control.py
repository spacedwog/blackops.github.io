# -----------------------------
# ai/voice_control.py
# -----------------------------
import speech_recognition as sr
from gtts import gTTS
import os
import tempfile
import requests
import pygame
from github import Github  # PyGithub
from transformers import pipeline  # HuggingFace model

# Setup: IA local + GitHub
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
github_token = os.getenv("GITHUB_TOKEN")
g = Github(github_token)

def speak(text):
    tts = gTTS(text=text, lang='pt-br')
    with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as fp:
        tts.save(fp.name)
        pygame.mixer.init()
        pygame.mixer.music.load(fp.name)
        pygame.mixer.music.play()
        while pygame.mixer.music.get_busy():
            continue
        pygame.mixer.quit()
        os.remove(fp.name)

def ask_github_ai(question):
    if "último commit" in question.lower():
        repo = g.get_repo("openai/whisper")
        commit = repo.get_commits()[0]
        return f"O último commit foi de {commit.commit.author.name}: {commit.commit.message}"
    elif "resumo" in question.lower():
        repo = g.get_repo("openai/whisper")
        readme = repo.get_readme().decoded_content.decode()
        summary = summarizer(readme[:1024], max_length=60, min_length=30, do_sample=False)
        return summary[0]['summary_text']
    else:
        return "Não entendi a pergunta sobre o GitHub."

def activate_voice_control():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Fale algo relacionado ao GitHub.")
        audio = recognizer.listen(source)
        try:
            comando = recognizer.recognize_google(audio, language="pt-BR")
            speak("Consultando o GitHub com IA.")
            resposta = ask_github_ai(comando)
            speak(resposta)
            return f"Você disse: {comando}\nGitHub respondeu: {resposta}"
        except sr.UnknownValueError:
            erro = "Não entendi o que você disse."
            speak(erro)
            return erro
        except sr.RequestError:
            erro = "Erro na API de reconhecimento."
            speak(erro)
            return erro