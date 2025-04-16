# -----------------------------
# network/port_scanner.py
# -----------------------------
import socket

def scan_ports(host='127.0.0.1', ports=range(443, 8501, 8502)):
    open_ports = []
    for port in ports:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.settimeout(0.5)
            result = s.connect_ex((host, port))
            if result == 0:
                open_ports.append(port)
    return open_ports