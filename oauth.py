import streamlit as st
import requests
import json
import urllib.parse

def get_google_auth_url(config):
    base_url = "https://accounts.google.com/o/oauth2/v2/auth"
    params = {
        "client_id": config["client_id"],
        "response_type": "code",
        "redirect_uri": config["redirect_uri"],
        "scope": " ".join(config["scope"]),
        "access_type": "offline",
        "prompt": "consent"
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
    r = requests.post(token_url, data=data)
    return r.json()

def get_user_info(access_token):
    r = requests.get("https://www.googleapis.com/oauth2/v2/userinfo", headers={"Authorization": f"Bearer {access_token}"})
    return r.json()