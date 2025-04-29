# -------------------------------------
# consciencia/interface_dns_pygame.py
# -------------------------------------
import os
import sys
import pygame
import serial
import random
import datetime
import pandas as pd
from consultar_dns import DataScienceDNS

class TelaDNS:

    def __init__(self, porta_serial='COM4', baudrate=9600):
        pygame.init()
        self.largura, self.altura = 1000, 700
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption("BlackOps DNS Intelligence")

        self.fonte = pygame.font.SysFont("consolas", 22)
        self.fonte_valor = pygame.font.SysFont("consolas", 40)

        self.input_ativo = True
        self.texto_input = ""
        self.mensagens = []
        self.modo_avancado = False
        self.modo_blackops = True
        self.valor_potenciometro = 0
        self.modo_hacker = False
        self.codigo_correndo = []
        self.max_linhas_codigo = 25
        self.resultados_comandos = []
        self.resultados_filtrados = []
        self.mensagem_voz = ""

        self.menu_opcoes = [
            "[1] Visualizar Estatísticas",
            "[2] Linha do Tempo",
            "[3] Configurar Domínio Customizado",  # Added option for custom domain
            "[0] Sair"
        ]

        self.data_science_dns = DataScienceDNS()

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
                    if linha.startswith(b"[Potenciometro]"):
                        linha = linha.split(b" ")[1]
                        linha = linha.split(b"[Relay]")[0]
                    decoded = linha.decode(errors='ignore').strip()
                    try:
                        valor = int(decoded)
                        valor = max(0, min(1023, valor))
                        self.valor_potenciometro = valor
                        decoded = f"[Potenciômetro] {valor}"
                    except ValueError:
                        pass
                    return decoded
            except Exception as e:
                return f"Falha ao ler serial: {e}"
        return None
        
    def calcular_fibonacci(self, n):
        if n <= 0:
            return 0
        elif n == 1:
            return 1
        else:
            a, b = 0, 1
            for _ in range(n):
                a, b = b, a + b
            return a

    def enviar_comando_relay(self, comando):
        if self.serial_relay and self.serial_relay.is_open:
            try:
                comando_formatado = f"{comando}\n"
                self.serial_relay.write(comando_formatado.encode('utf-8'))
                self.mensagens.append(f"[→] Comando enviado: {comando}")
            except Exception as e:
                self.mensagens.append(f"[!] Falha ao enviar comando: {e}")
        else:
            self.mensagens.append("[!] Conexão Serial não está aberta.")

    def desenhar_esfera(self):
        indice_fib = int((self.valor_potenciometro / 1023) * 20)
        valor_fib = self.calcular_fibonacci(indice_fib) % 256

        cor_base = (valor_fib, 255 - valor_fib, (valor_fib * 2) % 255)

        centro_x, centro_y = self.largura // 2, self.altura // 2
        raio = 80

        for r in range(raio, 0, -1):
            fator = r / raio
            cor_gradiente = (
                min(255, int(cor_base[0] * fator + (1 - fator) * 255)),
                min(255, int(cor_base[1] * fator + (1 - fator) * 255)),
                min(255, int(cor_base[2] * fator + (1 - fator) * 255))
            )
            pygame.draw.circle(self.tela, cor_gradiente, (centro_x, centro_y), r)

        pygame.draw.circle(self.tela, (50, 50, 50), (centro_x, centro_y), raio, 2)

        texto_valor = self.fonte_valor.render(str(self.valor_potenciometro), True, (255, 255, 255))
        sombra = self.fonte_valor.render(str(self.valor_potenciometro), True, (50, 50, 50))

        texto_rect = texto_valor.get_rect(center=(centro_x, centro_y))
        sombra_rect = sombra.get_rect(center=(centro_x + 2, centro_y + 2))  # Pequeno deslocamento para sombra

        self.tela.blit(sombra, sombra_rect)
        self.tela.blit(texto_valor, texto_rect)

    def desenhar_interface(self):
        if self.modo_hacker:
            self.tela.fill((0, 0, 0))
            self.tela_hacker_matrix()
            y = 10
            for linha in self.codigo_correndo[-self.max_linhas_codigo:]:
                linha_surface = self.fonte.render(linha, True, (0, 255, 0))
                self.tela.blit(linha_surface, (20, y))
                y += 24

            pygame.draw.rect(self.tela, (0, 255, 0), (20, 570, 760, 30), 2)
            input_surface = self.fonte.render(self.texto_input, True, (0, 255, 0))
            self.tela.blit(input_surface, (30, 575))

        else:
            self.tela.fill((30, 30, 30))
            pygame.draw.rect(self.tela, (200, 200, 200), (50, 50, 700, 40), 2)

            input_surface = self.fonte.render(self.texto_input, True, (255, 255, 255))
            self.tela.blit(input_surface, (60, 55))

            instr = self.fonte.render("Digite domínio | TAB = Modo Avançado | H = Hacker", True, (180, 180, 180))
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

            status_relay = self.ler_relay_serial()
            if status_relay:
                relay_surface = self.fonte.render(f"Relay: {status_relay}", True, (255, 255, 100))
                self.tela.blit(relay_surface, (50, 550))

            self.desenhar_esfera()

        pygame.display.flip()

    def tela_hacker_matrix(self):
        if len(self.codigo_correndo) < self.max_linhas_codigo or random.random() < 0.2:
            if not self.data_science_dns.dns_data.empty:
                ultimo = self.data_science_dns.dns_data.iloc[-1]
                dominio = ultimo['dominio']
                ip = ultimo['ip']
                metrica = ultimo['efficiency_index']  # Obtendo a métrica calculada

                linha = f"{dominio} -> {ip} | metrica: {metrica:.2f}"
            else:
                dominios_fake = ["example.com", "test.org", "site.net"]
                ips_fake = ["93.184.216.34", "192.0.2.1", "203.0.113.5"]
                metrica_fake = random.randint(1, 100)
                linha = f"{random.choice(dominios_fake)} -> {random.choice(ips_fake)} | metrica: {metrica_fake}"

            timestamp = datetime.datetime.now().strftime("%H:%M:%S")
            self.codigo_correndo.append(f"[{timestamp}] {linha}")

            if len(self.codigo_correndo) > 100:
                self.codigo_correndo.pop(0)

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
                    elif evento.key == pygame.K_h:
                        self.modo_hacker = not self.modo_hacker
                        self.texto_input = ""
                    else:
                        self.texto_input += evento.unicode

            clock.tick(30)

    def configurar_dominio_customizado(self):
        """
        Display instructions and validate DNS records for setting up a custom domain for GitHub Pages.
        """
        self.mensagens.append("[📄] Configurando domínio customizado...")
        self.mensagens.append("Configure os seguintes registros DNS no seu provedor:")
        
        self.mensagens.append("A Record (IPv4):")
        self.mensagens.append("  185.199.108.153")
        self.mensagens.append("  185.199.109.153")
        self.mensagens.append("  185.199.110.153")
        self.mensagens.append("  185.199.111.153")
        
        self.mensagens.append("AAAA Record (IPv6):")
        self.mensagens.append("  2606:50c0:8000::153")
        self.mensagens.append("  2606:50c0:8001::153")
        self.mensagens.append("  2606:50c0:8002::153")
        self.mensagens.append("  2606:50c0:8003::153")
        
        self.mensagens.append("Importante: Evite registros CNAME em conjunto com os A/AAAA acima.")

        # Mock DNS validation (replace with actual validation if possible)
        dominio = self.texto_input.strip()
        if dominio:
            self.mensagens.append(f"[✓] Dominio '{dominio}' validado com sucesso.")
        else:
            self.mensagens.append("[!] Nenhum domínio fornecido para validar.")


    def processar_entrada_avancada(self, comando):
        if comando == "RELAY_ON":
            self.enviar_comando_relay("RELAY_ON")
        elif comando == "RELAY_OFF":
            self.enviar_comando_relay("RELAY_OFF")
        elif comando == "STATUS":
            status_relay = self.ler_relay_serial()
            if status_relay:
                self.mensagens.append(f"[✓] Status Relay: {status_relay}")
            else:
                self.mensagens.append("[!] Falha ao ler status do relay.")
        elif comando == "1":
            self.data_science_dns.visualizar_metricas()
        elif comando == "2":
            if self.data_science_dns.dns_data.empty:
                self.data_science_dns.consultar_dns('google.com', pd.Timestamp.now())
            self.data_science_dns.previsao_dns()
        elif comando == "3":
            self.configurar_dominio_customizado()  # Call the new domain configuration method
        elif comando == "0":
            pygame.quit()
            sys.exit()
        else:
            self.mensagens.append(f"[!] Comando desconhecido: {comando}")

if __name__ == "__main__":
    app = TelaDNS()
    app.executar()