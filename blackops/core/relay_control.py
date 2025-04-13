# -----------------------------
# core/relay_control.py
# -----------------------------
import platform

if platform.system() == "Linux":
    from gpiozero import LED
    from time import sleep
    RELAY_PIN = 5
    relay = LED(RELAY_PIN)

    def activate_relay():
        relay.on()
        sleep(2)
        relay.off()
else:
    def activate_relay():
        print("Simulação: Relay ativado (modo desktop)")