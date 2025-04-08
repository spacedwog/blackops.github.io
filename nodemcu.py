# nodemcu.py
import requests

def enviar_para_esp8266(endpoint, payload):
    try:
        url = f"http://192.168.15.8/{endpoint}"
        r = requests.post(url, json=payload, timeout=5)
        return r.text
    except Exception as e:
        return str(e)