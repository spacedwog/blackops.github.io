import sys
import pygame

class TelaBlackOps:
    def __init__(self, largura=800, altura=600, titulo="Tela BlackOps - Pygame"):
        # Inicialização do Pygame
        pygame.init()
        pygame.font.init()

        # Propriedades da tela
        self.largura = largura
        self.altura = altura
        self.titulo = titulo
        self.fps = 60
        self.cor_fundo = (255, 255, 255)
        self.cor_texto = (0, 120, 255)

        # Configuração da janela
        self.tela = pygame.display.set_mode((self.largura, self.altura))
        pygame.display.set_caption(self.titulo)

        # Fonte
        self.fonte = pygame.font.SysFont("Arial", 36)

        # Relógio para controlar FPS
        self.clock = pygame.time.Clock()

        # Controle do loop principal
        self.rodando = True

    def desenhar(self):
        self.tela.fill(self.cor_fundo)

        # Texto central
        texto = self.fonte.render("Bem-vindo à BlackOps!", True, self.cor_texto)
        texto_rect = texto.get_rect(center=(self.largura // 2, self.altura // 2))
        self.tela.blit(texto, texto_rect)

        pygame.display.flip()

    def executar(self):
        while self.rodando:
            for evento in pygame.event.get():
                if evento.type == pygame.QUIT:
                    self.rodando = False

            self.desenhar()
            self.clock.tick(self.fps)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    tela_blackops = TelaBlackOps()
    tela_blackops.executar()