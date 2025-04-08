import requests

def enviar_para_esp8266(endpoint: str, payload: dict):
    url = f"http://192.168.15.8/{endpoint}"  # IP do NodeMCU
    try:
        r = requests.post(url, json=payload, timeout=2)
        return r.text
    except requests.RequestException as e:
        return f"Erro: {e}"