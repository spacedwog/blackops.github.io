# -----------------------------
# core/incident_logger.py
# -----------------------------
import datetime

def log_incident(message):
    with open("incident_log.txt", "a") as log:
        timestamp = datetime.datetime.now().isoformat()
        log.write(f"[{timestamp}] {message}\n")