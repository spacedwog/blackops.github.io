# ----------------------------
# tcp_server_streamlit.py
# ----------------------------
import socket
import streamlit as st
import subprocess
import threading

HOST = '192.168.15.8'
PORT = 8502

def handle_client(conn, addr):
    with conn:
        while True:
            data = conn.recv(1024)
            if not data:
                break
            command = data.decode()
            try:
                result = subprocess.check_output(command, shell=True, stderr=subprocess.STDOUT, text=True)
            except subprocess.CalledProcessError as e:
                result = e.output
            conn.sendall(result.encode())

def start_server():
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.bind((HOST, PORT))
    s.listen()
    while True:
        conn, addr = s.accept()
        client_thread = threading.Thread(target=handle_client, args=(conn, addr))
        client_thread.start()

st.title("Servidor TCP/IP com Streamlit")
st.write("Aguardando comandos do PowerShell...")

threading.Thread(target=start_server, daemon=True).start()