# -----------------------------
# consciencia/interface_dns_relay.py
# -----------------------------
import sys
import pygame
import serial
import datetime
import pandas as pd
import streamlit as st
from consultar_dns import DataScienceDNS

class TelaDNS:
    def __init__(self, porta_serial='COM4', baudrate=9600):
        # Inicializar Pygame
        pygame.init()
        self.largura, self.altura = 800, 600
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("Consulta DNS com Relay Serial")

        # Fonte
        self.fonte = pygame.font.SysFont("consolas", 24)

        # Estado
        self.input_ativo = True
        self.texto_input = ""
        self.mensagens = []
        self.modo_avancado = False

        # Opções do menu
        self.menu_opcoes = [
            "[1] Visualizar Estatísticas",
            "[2] Previsão DNS",
            "[3] Detecção de Anomalias",
            "[4] Clusterização",
            "[5] Exportar CSV",
            "[6] Exportar MongoDB",
            "[7] Agendar Coletas"
        ]

        # Classe de Data Science
        self.data_science_dns = DataScienceDNS()

        # Inicializar conexão Serial Relay
        self.porta_serial = porta_serial
        self.baudrate = baudrate
        try:
            self.serial_relay = serial.Serial(self.porta_serial, self.baudrate, timeout=1)
            self.mensagens.append("[✓] Conexão Serial Relay estabelecida.")
        except Exception as e:
            self.serial_relay = None
            self.mensagens.append(f"[!] Falha ao conectar Serial: {e}")

    def ler_relay_serial(self):
        if self.serial_relay and self.serial_relay.is_open:
            try:
                linha = self.serial_relay.readline()
                if linha:
                    decoded = linha.decode(errors='ignore').strip()
                    return decoded
            except Exception as e:
                return f"Falha ao ler serial: {e}"
        return None

    def desenhar_interface(self):
        self.tela.fill((30, 30, 30))
        pygame.draw.rect(self.tela, (200, 200, 200), (50, 50, 700, 40), 2)

        input_surface = self.fonte.render(self.texto_input, True, (255, 255, 255))
        self.tela.blit(input_surface, (60, 55))

        instr = self.fonte.render("Digite domínio | TAB = Modo Avançado", True, (180, 180, 180))
        self.tela.blit(instr, (50, 10))

        y = 120
        if self.modo_avancado:
            self.tela.blit(self.fonte.render("🔍 Modo Avançado:", True, (255, 200, 100)), (50, y))
            y += 40
            for opcao in self.menu_opcoes:
                msg_surface = self.fonte.render(opcao, True, (100, 255, 250))
                self.tela.blit(msg_surface, (70, y))
                y += 30
        else:
            for mensagem in self.mensagens[-10:]:
                msg_surface = self.fonte.render(mensagem, True, (200, 255, 200))
                self.tela.blit(msg_surface, (50, y))
                y += 30

        # Mostrar status relay lido
        status_relay = self.ler_relay_serial()
        if status_relay:
            relay_surface = self.fonte.render(f"Relay: {status_relay}", True, (255, 255, 100))
            self.tela.blit(relay_surface, (50, 550))

        pygame.display.flip()

    def executar(self):
        clock = pygame.time.Clock()

        while True:
            self.desenhar_interface()

            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    if self.serial_relay:
                        self.serial_relay.close()
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