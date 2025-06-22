import pygame
import sys

# === CONFIGURAÇÃO BÁSICA ===
pygame.init()
largura, altura = 800, 600
tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Menu Principal")
fonte = pygame.font.Font(None, 48)
clock = pygame.time.Clock()

cores = {
    "fundo": (30, 30, 30),
    "branco": (255, 255, 255),
    "preto": (0, 0, 0),
    "azul": (0, 120, 255),
    "azul_escuro": (0, 55, 100),
    "cinza": (120, 120, 120),
    "hover": (0, 180, 255)
}

# === BOTÃO GENÉRICO ===
class Botao:
    def __init__(self, texto, x, y, largura, altura, acao=None):
        self.texto = texto
        self.rect = pygame.Rect(x, y, largura, altura)
        self.acao = acao

    def desenhar(self, tela, mouse_pos):
        cor = cores["hover"] if self.rect.collidepoint(mouse_pos) else cores["azul"]
        pygame.draw.rect(tela, cor, self.rect)
        pygame.draw.rect(tela, cores["preto"], self.rect, 2)
        texto_render = fonte.render(self.texto, True, cores["branco"])
        tela.blit(texto_render, texto_render.get_rect(center=self.rect.center))

    def checar_clique(self, mouse_pos):
        if self.rect.collidepoint(mouse_pos) and self.acao:
            self.acao()

# === TELA DE MENU ===
tela_largura, tela_altura = 700, 500
tela_x = (largura - tela_largura) // 2
tela_y = (altura - tela_altura) // 2

# === FUNÇÕES DE AÇÃO ===
def jogar():
    import jogadorEfluxo
    jogadorEfluxo.executar()

def instrucoes():
    fonte_menor = pygame.font.Font(None, 32)

    texto_linhas = [
        "OBJETIVO:",
        "Responda corretamente as operações",
        "matemáticas dentro do tempo!",
        "",
        "- Use as SETAS do teclado para se mover pelo tabuleiro.",
        "- Erros tiram uma vida. Você tem 3!",
        "",
        "Boa sorte!"
    ]

    botao_voltar = Botao("Voltar", tela_x + 225, tela_y + 410, 250, 50, menu_principal)

    rodando = True
    while rodando:
        pygame.draw.rect(tela, cores["azul_escuro"], (tela_x-4, tela_y-4, tela_largura+8, tela_altura+8))
        pygame.draw.rect(tela, cores["preto"], (tela_x, tela_y, tela_largura, tela_altura))

        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if botao_voltar.rect.collidepoint(mouse_pos):
                    rodando = False

        for i, linha in enumerate(texto_linhas):
            if linha in ["OBJETIVO:", "Boa sorte!"]:
                fonte_destaque = pygame.font.Font(None, 40)
                texto_render = fonte_destaque.render(linha, True, cores["hover"])
            else:
                texto_render = fonte_menor.render(linha, True, cores["branco"])
        
            tela.blit(texto_render, (largura//2 - texto_render.get_width()//2, 120 + i*35))

        botao_voltar.desenhar(tela, mouse_pos)

        pygame.display.flip()
        clock.tick(60)

def opcoes():
    import config
    tempos = [10, 15, 20]
    rodadas = list(range(3, 21))
    sons = ["Ligado", "Desligado"]

    tempo_index = tempos.index(config.tempo_limite)
    rodada_index = rodadas.index(config.total_rodada)
    som_index = 0 if config.som_ativo else 1
    fonte_grande = pygame.font.Font(None, 64)
    botao_voltar = Botao("Voltar", tela_x + 225, tela_y + 410, 250, 50, menu_principal)

    rodando = True
    while rodando:
        tela.fill(cores["preto"])
        mouse_pos = pygame.mouse.get_pos()

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair()
            elif evento.type == pygame.MOUSEBUTTONDOWN:
                if seta_esq_tempo.collidepoint(mouse_pos) and tempo_index > 0:
                    tempo_index -= 1
                    config.tempo_limite = tempos[tempo_index]
                if seta_dir_tempo.collidepoint(mouse_pos) and tempo_index < len(tempos) - 1:
                    tempo_index += 1
                    config.tempo_limite = tempos[tempo_index]

                if seta_esq_rodada.collidepoint(mouse_pos) and rodada_index > 0:
                    rodada_index -= 1
                    config.total_rodada = rodadas[rodada_index]
                if seta_dir_rodada.collidepoint(mouse_pos) and rodada_index < len(rodadas) - 1:
                    rodada_index += 1
                    config.total_rodada = rodadas[rodada_index]

                if seta_esq_som.collidepoint(mouse_pos) and som_index > 0:
                    som_index -= 1
                    config.som_ativo = (som_index == 0)
                if seta_dir_som.collidepoint(mouse_pos) and som_index < len(sons) - 1:
                    som_index += 1
                    config.som_ativo = (som_index == 0)

                if botao_voltar.rect.collidepoint(mouse_pos):
                    rodando = False

        titulo = fonte_grande.render("Opções", True, cores["branco"])
        tela.blit(titulo, (largura // 2 - titulo.get_width() // 2, 40))

        y_base = 150

        def desenhar_opcao(texto, valor, index, valores, y, dist_setas):
            label = fonte.render(texto, True, cores["branco"])
            tela.blit(label, (120, y))

            x_centro = 600
            seta_esq = pygame.Rect(x_centro - dist_setas - 30, y, 30, 40)
            seta_dir = pygame.Rect(x_centro + dist_setas, y, 30, 40)

            valor_render = fonte.render(str(valor), True, cores["branco"])
            valor_rect = valor_render.get_rect(center=(x_centro, y + 20))
            tela.blit(valor_render, valor_rect)

            pygame.draw.polygon(tela, cores["branco"] if index > 0 else cores["cinza"],
                                [(seta_esq.centerx + 5, y + 10), (seta_esq.centerx - 5, y + 20), (seta_esq.centerx + 5, y + 30)])
            pygame.draw.polygon(tela, cores["branco"] if index < len(valores) - 1 else cores["cinza"],
                                [(seta_dir.centerx - 5, y + 10), (seta_dir.centerx + 5, y + 20), (seta_dir.centerx - 5, y + 30)])

            return seta_esq, seta_dir

        # Tempo
        seta_esq_tempo, seta_dir_tempo = desenhar_opcao("Tempo por rodada:", tempos[tempo_index], tempo_index, tempos, y_base, dist_setas=35)

        # Rodadas
        y_base += 70
        seta_esq_rodada, seta_dir_rodada = desenhar_opcao("Quantidade de rodadas:", rodadas[rodada_index], rodada_index, rodadas, y_base, dist_setas=35)

        # Som
        y_base += 70
        seta_esq_som, seta_dir_som = desenhar_opcao("Som:", sons[som_index], som_index, sons, y_base, dist_setas=90)

        botao_voltar.desenhar(tela, mouse_pos)

        pygame.display.flip()
        clock.tick(60)

def sair():
    pygame.quit()
    sys.exit()

# === CRIAR BOTÕES ===
botoes = [
    Botao("Jogar",       275, 200, 250, 60, jogar),
    Botao("Instruções",  275, 290, 250, 60, instrucoes),
    Botao("Opções",      275, 380, 250, 60, opcoes),
    Botao("Sair",        275, 470, 250, 60, sair)
]

# === CRIAR TITULO ===
fonte_titulo = pygame.font.Font(None, 84)
titulo_jogo = fonte_titulo.render("ColorBlock & Matemática", True, (255, 165, 0))

# === LOOP DO MENU ===
def menu_principal():
    while True:
        tela.fill(cores["fundo"])
        mouse_pos = pygame.mouse.get_pos()
        tela.blit(titulo_jogo, (largura // 2 - titulo_jogo.get_width() // 2, 80))


        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                sair()
            if evento.type == pygame.MOUSEBUTTONDOWN:
                for botao in botoes:
                    botao.checar_clique(mouse_pos)

        for botao in botoes:
            botao.desenhar(tela, mouse_pos)

        pygame.display.flip()
        clock.tick(60)

menu_principal()