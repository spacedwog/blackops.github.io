# -----------------------------
# consciencia/interface_dns_pygame.py
# -----------------------------
import sys
import pygame
import serial
import datetime
import threading
import pandas as pd
import serial.tools.list_ports
from consultar_dns import DataScienceDNS

class TelaDNS:
    def __init__(self):
        pygame.init()
        self.serial_relay = None
        self.iniciar_serial_relay()


        self.largura, self.altura = 800, 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Consulta DNS Interativa")

        self.fonte = pygame.font.SysFont("consolas", 24)
        self.input_ativo = True
        self.texto_input = ""
        self.mensagens = []
        self.modo_avancado = False  # << Ativa modo avançado
        self.menu_opcoes = [
            "[1] Visualizar Estatísticas",
            "[2] Previsão DNS",
            "[3] Detecção de Anomalias",
            "[4] Clusterização",
            "[5] Exportar CSV",
            "[6] Exportar MongoDB",
            "[7] Agendar Coletas"
        ]
        self.data_science_dns = DataScienceDNS()

    def iniciar_serial_relay(self, porta='COM4', baudrate=9600):
        try:
            self.serial_relay = serial.Serial(porta, baudrate, timeout=1)
            print(f"[✓] Conectado na porta {porta}")
        except Exception as e:
            print(f"[Erro] Falha ao abrir serial {porta}: {e}")

    def ler_serial(self):
        while True:
            if self.serial_port and self.serial_port.is_open:
                try:
                    linha = self.serial_port.readline().decode('utf-8').strip()
                    if linha:
                        print(f"[Serial] {linha}")  # (opcional: debug no terminal)
                        self.relay_mensagens.append(linha)
                        
                        # Se quiser também exibir na interface normal:
                        self.mensagens.append(linha)
                except Exception as e:
                    print(f"[Erro] Leitura Serial: {e}")

    def iniciar_serial_relay(self, porta='COM4', baudrate=9600):
        try:
            self.serial_relay = serial.Serial(porta, baudrate, timeout=1)
            print(f"[✓] Conectado na porta {porta}")
        except Exception as e:
            print(f"[Erro] Falha ao abrir serial {porta}: {e}")

    def desenhar_interface(self):
        self.tela.fill((30, 30, 30))
        pygame.draw.rect(self.tela, (200, 200, 200), (50, 50, 700, 40), 2)

        input_surface = self.fonte.render(self.texto_input, True, (255, 255, 255))
        self.tela.blit(input_surface, (60, 55))

        instr = self.fonte.render("Digite um domínio e pressione Enter | TAB = Avançado", True, (180, 180, 180))
        self.tela.blit(instr, (50, 10))

        relay_status = self.ler_relay_serial()
        relay_surface = self.fonte.render(f"Relay: {relay_status}", True, (255, 180, 180))
        self.tela.blit(relay_surface, (50, 90))

        y = 120
        if self.modo_avancado:
            self.tela.blit(self.fonte.render("🔍 Modo Avançado Ativo:", True, (255, 200, 100)), (50, y))
            y += 40
            for opcao in self.menu_opcoes:
                msg_surface = self.fonte.render(opcao, True, (100, 255, 250))
                self.tela.blit(msg_surface, (70, y))
                y += 30
        else:
            for mensagem in self.mensagens[-10:]:
                msg_surface = self.fonte.render(mensagem, True, (200, 255, 200))
                self.tela.blit(msg_surface, (50, y))
                y += 20
                self.tela.blit(self.fonte.render("Relays:", True, (255, 200, 100)), (50, y))
                y += 30
                for relay_msg in self.relay_mensagens[-4:]:  # Últimas 4 mensagens do relay
                    msg_surface = self.fonte.render(relay_msg, True, (255, 255, 100))
                    self.tela.blit(msg_surface, (70, y))
                    y += 30

        pygame.display.flip()


    def executar(self):
        clock = pygame.time.Clock()

        while True:
            self.desenhar_interface()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if evento.type == pygame.KEYDOWN:
                    if evento.key == pygame.K_RETURN:
                        if not self.modo_avancado:
                            dominio = self.texto_input.strip()
                            if dominio:
                                timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                                self.data_science_dns.consultar_dns(dominio, timestamp)
                                resultado = f"{dominio} -> {self.data_science_dns.dns_data.iloc[-1]['ip']}"
                                self.mensagens.append(resultado)
                        else:
                            self.processar_entrada_avancada(self.texto_input.strip())
                        self.texto_input = ""

                    elif evento.key == pygame.K_TAB:
                        self.modo_avancado = not self.modo_avancado
                        self.texto_input = ""

                    elif evento.key == pygame.K_BACKSPACE:
                        self.texto_input = self.texto_input[:-1]
                    else:
                        self.texto_input += evento.unicode

            clock.tick(30)

    def processar_entrada_avancada(self, comando):
        if comando == "1":
            self.data_science_dns.visualizar_metricas()
        elif comando == "2":
            if self.data_science_dns.dns_data.empty:
                self.data_science_dns.consultar_dns('google.com', pd.Timestamp.now())
            self.data_science_dns.previsao_dns()
        elif comando == "3":
            if self.data_science_dns.dns_data.empty:
                self.data_science_dns.consultar_dns('google.com', pd.Timestamp.now())
            self.data_science_dns.detectar_anomalias()
        elif comando == "4":
            if self.data_science_dns.dns_data.empty:
                self.data_science_dns.consultar_dns('google.com', pd.Timestamp.now())
            self.data_science_dns.clusterizar_dns()
        elif comando == "5":
            if self.data_science_dns.dns_data.empty:
                self.data_science_dns.consultar_dns('google.com', pd.Timestamp.now())
            self.data_science_dns.exportar_csv()
            self.mensagens.append("[✓] Dados exportados para CSV")
        elif comando == "6":
            if self.data_science_dns.dns_data.empty:
                self.data_science_dns.consultar_dns('google.com', pd.Timestamp.now())
            uri = "mongodb+srv://twitchcombopunch:6z2h1j3k9F.@clusterops.iodjyeg.mongodb.net/"
            db = "clusterops"
            collection = "dns_logs"
            self.data_science_dns.exportar_mongodb(uri, db, collection)
            self.mensagens.append("[✓] Dados exportados para MongoDB")
        elif comando == "7":
            dominio = self.texto_input.strip()
            if dominio:
                self.data_science_dns.agendar_coleta(dominio)
                self.mensagens.append(f"[✓] Coletas agendadas para {dominio}")
            else:
                self.mensagens.append("[!] Digite um domínio antes de agendar")
        else:
            self.mensagens.append(f"[!] Comando inválido: {comando}")

if __name__ == "__main__":
    app = TelaDNS()
    app.executar()