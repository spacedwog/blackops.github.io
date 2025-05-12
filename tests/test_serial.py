import serial

print(serial.__file__)  # Mostra o caminho do módulo carregado
s = serial.Serial('COM3', 9600, timeout=1)
print("OK: Conectado com sucesso!")