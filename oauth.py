# oauth.py
import requests
import urllib.parse

def get_google_auth_url(config):
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "response_type": "code",
        "client_id": config["client_id"],
        "redirect_uri": config["redirect_uri"],
        "scope": " ".join(config["scope"]),
        "access_type": "offline"
    }
    return f"{base_url}?{urllib.parse.urlencode(params)}"

def get_tokens(code, config):
    token_url = "https://oauth2.googleapis.com/token"
    data = {
        "code": code,
        "client_id": config["client_id"],
        "client_secret": config["client_secret"],
        "redirect_uri": config["redirect_uri"],
        "grant_type": "authorization_code"
    }
    response = requests.post(token_url, data=data)
    if response.status_code == 200:
        return response.json()
    else:
        print("Erro ao trocar código por token:", response.text)
        return {}

def get_user_info(access_token):
    headers = {"Authorization": f"Bearer {access_token}"}
    r = requests.get("https://www.googleapis.com/oauth2/v1/userinfo", headers=headers)
    return r.json()