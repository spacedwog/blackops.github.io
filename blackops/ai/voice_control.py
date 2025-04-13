# -----------------------------
# ai/voice_control.py
# -----------------------------
import speech_recognition as sr

def activate_voice_control():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Fale algo...")
        audio = recognizer.listen(source)
        try:
            comando = recognizer.recognize_google(audio, language="pt-BR")
            return f"Comando reconhecido: {comando}"
        except sr.UnknownValueError:
            return "Não entendi o que você disse."
        except sr.RequestError:
            return "Erro na API de reconhecimento."