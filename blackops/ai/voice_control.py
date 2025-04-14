# -----------------------------
# ai/voice_control.py
# -----------------------------
import pyttsx3
import speech_recognition as sr

def speak(texto):
    engine = pyttsx3.init()
    engine.setProperty("rate", 170)  # Velocidade da fala
    engine.setProperty("volume", 1.0)
    engine.say(texto)
    engine.runAndWait()

def activate_voice_control():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        speak("Fale algo.")
        print("Fale algo...")
        audio = recognizer.listen(source)

        try:
            comando = recognizer.recognize_google(audio, language="pt-BR")
            resposta = f"Comando reconhecido: {comando}"
            speak(comando)
            return resposta
        except sr.UnknownValueError:
            erro = "Não entendi o que você disse."
            speak(erro)
            return erro
        except sr.RequestError:
            erro = "Erro na API de reconhecimento."
            speak(erro)
            return erro