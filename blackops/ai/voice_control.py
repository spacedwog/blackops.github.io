# -----------------------------
# ai/voice_control.py
# -----------------------------
import speech_recognition as sr
from gtts import gTTS
import os
import pygame
import tempfile
import requests

from github import Github  # PyGithub
from transformers import pipeline  # HuggingFace model

# Setup: IA local + GitHub
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")
github_token = os.getenv("8928341d3b422e184b621364a45885f6a2baa804")
g = Github(github_token)

def normalizar_comando(comando):
    comando = comando.lower()

    # Mapeamento de termos falados para termos técnicos do GitHub
    mapeamento = {
        "comite": "commit",
        "comitê": "commit",
        "commite": "commit",
        "última atualização": "último commit",
        "última modificação": "último commit",
        "requisição de puxar": "pull request",
        "por request": "pull request",
        "pau request": "pull request",
        "resumo do repositório": "resumo",
        "problemas abertos": "issues",
        "quantas issues": "issues",
        "erro": "issues",
        "linguagem": "linguagem principal",
        "qual linguagem": "linguagem principal",
        "quem criou": "criador",
        "dono do repositório": "criador",
        "quantas estrelas": "estrelas",
        "número de estrelas": "estrelas",
    }

    for errado, certo in mapeamento.items():
        if errado in comando:
            comando = comando.replace(errado, certo)

    return comando

def speak(text):
    tts = gTTS(text=text, lang='pt-br')
    temp_path = os.path.join(tempfile.gettempdir(), "voz.mp3")
    tts.save(temp_path)

    pygame.mixer.init()
    pygame.mixer.music.load(temp_path)
    pygame.mixer.music.play()
    while pygame.mixer.music.get_busy():
        continue
    pygame.mixer.quit()
    os.remove(temp_path)

def ask_github_ai(question):
    repo = g.get_repo("openai/whisper")

    if "commit" in question:
        commit = repo.get_commits()[0]
        return f"O último commit foi de {commit.commit.author.name}: {commit.commit.message}"

    elif "resumo" in question:
        readme = repo.get_readme().decoded_content.decode()
        summary = summarizer(readme[:1024], max_length=60, min_length=30, do_sample=False)
        return summary[0]['summary_text']

    elif "linguagem principal" in question:
        return f"A linguagem principal do repositório é {repo.language}."

    elif "estrelas" in question:
        return f"O repositório possui {repo.stargazers_count} estrelas."

    elif "issues" in question:
        return f"O número de issues abertas é {repo.open_issues_count}."

    elif "criador" in question:
        return f"O criador do repositório é {repo.owner.login}."

    else:
        return "Não entendi a pergunta sobre o GitHub."

# ---------------------------
# ALGORITMOS GITHUB AUXILIARES
# ---------------------------

def get_last_commit(repo_name):
    repo = g.get_repo(repo_name)
    commit = repo.get_commits()[0]
    return f"O último commit foi de {commit.commit.author.name}: {commit.commit.message}"

def summarize_repo(repo_name):
    repo = g.get_repo(repo_name)
    readme = repo.get_readme().decoded_content.decode()
    summary = summarizer(readme[:1024], max_length=60, min_length=30, do_sample=False)
    return summary[0]['summary_text']

def count_issues(repo_name):
    repo = g.get_repo(repo_name)
    issues = repo.get_issues(state='open')
    return f"O repositório tem {issues.totalCount} issues abertas."

def list_pull_requests(repo_name):
    repo = g.get_repo(repo_name)
    pulls = repo.get_pulls(state='open', sort='created')
    if pulls.totalCount == 0:
        return "Não há pull requests abertas."
    lista = [f"- {pr.title} por {pr.user.login}" for pr in pulls[:3]]
    return "Pull requests abertas:\n" + "\n".join(lista)

def repo_language(repo_name):
    repo = g.get_repo(repo_name)
    lang = repo.language
    return f"O repositório foi escrito principalmente em {lang}."

def activate_voice_control():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Fale algo relacionado ao GitHub.")
        audio = recognizer.listen(source)
        try:
            comando = recognizer.recognize_google(audio, language="pt-BR")
            speak("Consultando o GitHub com IA.")

            comando_normalizado = normalizar_comando(comando)
            resposta = ask_github_ai(comando_normalizado)
            
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