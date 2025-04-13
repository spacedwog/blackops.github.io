# -----------------------------
# network/net_status.py
# -----------------------------
import os

def ping(host="127.0.0.1"):
    response = os.system(f"ping -c 1 {host}")
    return response == 0