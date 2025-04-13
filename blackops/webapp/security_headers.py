# -----------------------------
# webapp/security_headers.py
# -----------------------------
import requests

def check_headers(url):
    response = requests.get(url)
    return response.headers