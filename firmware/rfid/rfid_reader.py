# -----------------------------
# rfid/rfid_reader.py
# -----------------------------
import time
import serial

class RFIDTagReader:
    def __init__(self, port='COM3', baudrate=9600, timeout=1):
        """
        Inicializa a comunicação serial com o leitor RFID 125kHz.

        :param port: Porta serial (ex: 'COM3' no Windows ou '/dev/ttyUSB0' no Linux)
        :param baudrate: Velocidade de comunicação serial
        :param timeout: Tempo de espera para leitura
        """
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.serial_conn = serial.Serial(port, baudrate, timeout=timeout)
        print(f"[INFO] Conectado ao leitor RFID na porta {port}")

    def read_tag(self):
        """
        Lê a tag RFID do cartão 125kHz (10 bytes / 12 caracteres com \r\n).
        :return: UID da tag ou None
        """
        if self.serial_conn.in_waiting:
            data = self.serial_conn.read(14)  # RDM6300 envia 14 bytes por tag
            if data and len(data) >= 10:
                tag = data[1:11].hex().upper()
                return tag
        return None

    def wait_for_tag(self):
        """
        Loop bloqueante até uma tag válida ser lida.
        :return: UID da tag
        """
        print("[INFO] Aguardando tag RFID...")
        while True:
            tag = self.read_tag()
            if tag:
                print(f"[TAG DETECTADA] UID: {tag}")
                return tag
            time.sleep(0.1)

    def close(self):
        """Fecha a conexão serial."""
        self.serial_conn.close()
        print(f"[INFO] Conexão com {self.port} encerrada.")