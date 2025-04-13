# -----------------------------
# core/serial_handler.py
# -----------------------------
import serial

def send_serial_command(port, baudrate, command):
    with serial.Serial(port, baudrate, timeout=1) as ser:
        ser.write(command.encode())
        return ser.readline().decode()