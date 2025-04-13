# -----------------------------
# webapp/ssl_validator.py
# -----------------------------
import ssl, socket

def validate_ssl(domain):
    ctx = ssl.create_default_context()
    with ctx.wrap_socket(socket.socket(), server_hostname=domain) as s:
        s.connect((domain, 443))
        cert = s.getpeercert()
        return cert