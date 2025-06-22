import pygame
import random

# === Parte 1: Geração das expressões ===


def gerarOperacao(operador):
    tentativa = 0
    while tentativa < 10:
        if operador == '+':
            a = random.randint(5, 20)
            b = random.randint(5, 20)
            if a == b or a + b <= 10:
                tentativa += 1
                continue
            resultado = a + b

        elif operador == '-':
            a = random.randint(5, 20)
            b = random.randint(1, a)
            if a - b <= 3 or a == b:
                tentativa += 1
                continue
            resultado = a - b

        elif operador == '*':
            a = random.randint(2, 10)
            b = random.randint(2, 10)
            if a == b == 1:
                tentativa += 1
                continue
            resultado = a * b

        elif operador == '/':
            b = random.randint(2, 10)
            resultado = random.randint(2, 10)
            a = b * resultado
            if resultado == 1:
                tentativa += 1
                continue
            operador = '÷'
        else:
            return None

        expressao = f"{a} {operador} {b}"
        return expressao, resultado

    return None


def gerarVariasOperacoes(qtd=50):
    operadores = ['+', '-', '*', '/']
    contador = {'+': 0, '-': 0, '*': 0, '/': 0}
    expressoes = []

    while len(expressoes) < qtd:
        op = random.choice(operadores)
        if contador[op] >= 10:
            continue

        resultado = gerarOperacao(op)
        if resultado:
            expressao, valor = resultado
            expressoes.append((expressao, valor))
            contador[op] += 1

    return expressoes

# === Parte 2: Interface com Pygame ===


pygame.init()
largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("JOGO BLOCOS - Expressões")

# Perguntas
perguntas = [
    "12 + 7",
    "6 x 12",
    "14 / 7"
]

# Variáveis
vidas = 3
tempo_limite = 10
tempo_inicial = pygame.time.get_ticks()
tempo_terminado = False
rodada = 0
total_rodadas = len(perguntas)

# Cores
amarelo = (255, 255, 0)
vermelho = (255, 0, 0)
verde = (0, 255, 0)
azul = (0, 0, 255)
roxo = (128, 0, 128)
laranja = (255, 165, 0)
branco = (255, 255, 255)
tela_fundo = (0, 0, 0)
numero_cor = (255, 255, 255)

# Bloco
largura_bloco = 70
altura_bloco = 70
espaço = 33
fonte = pygame.font.Font(None, 36)

# Matriz de cores
matriz_cores = [
    [vermelho, amarelo, azul, verde, verde, vermelho, laranja, azul, verde, roxo],
    [verde, roxo, vermelho, amarelo, azul, verde, roxo, laranja, amarelo, azul],
    [amarelo, azul, verde, roxo, vermelho, amarelo, azul, verde, roxo, laranja],
    [azul, verde, roxo, vermelho, laranja, azul, verde, roxo, vermelho, amarelo],
    [roxo, vermelho, amarelo, azul, verde, roxo, laranja, amarelo, azul, verde]
]

expressoes_geradas = gerarVariasOperacoes(50)


def matriz_bloco(cores, expressoes):
    matriz = []
    idx = 0
    for linha_index, linha_cores in enumerate(cores):
        linha_blocos = []
        for coluna_index, cor in enumerate(linha_cores):
            x = coluna_index * (largura_bloco + espaço)
            y = linha_index * (altura_bloco + espaço)
            bloco_rect = pygame.Rect(x, y, largura_bloco, altura_bloco)

            # Pega expressão e resultado
            if idx < len(expressoes):
                expr, valor = expressoes[idx]
                texto = f"{valor}"
                idx += 1
            else:
                texto = "?"

            linha_blocos.append((bloco_rect, cor, texto))
        matriz.append(linha_blocos)
    return matriz


desenhar_matriz = matriz_bloco(matriz_cores, expressoes_geradas)

# Loop principal
rodar = True
while rodar:
    for evento in pygame.event.get():
        if evento.type == pygame.QUIT:
            rodar = False

    tela.fill(tela_fundo)

    if vidas > 0 and rodada < total_rodadas:
        tempo_atual = pygame.time.get_ticks()
        tempo_decorrido = (tempo_atual - tempo_inicial) // 1000
        tempo_restante = max(0, tempo_limite - tempo_decorrido)

        # Se o tempo acabou, perde uma vida e reinicia o tempo
        if tempo_restante == 0 and not tempo_terminado:
            vidas -= 1
            rodada += 1
            tempo_inicial = pygame.time.get_ticks()
            tempo_terminado = True

        # Reinicia controle de tempo terminado após 1 segundo
        if tempo_terminado and (pygame.time.get_ticks() - tempo_inicial) > 1000:
            tempo_terminado = False

        # Exibe tempo e vidas
        texto_tempo = fonte.render(f"Tempo: {tempo_restante}", True, branco)
        texto_vidas = fonte.render(f"Vidas restantes: {vidas}", True, branco)
        texto_pergunta = fonte.render(perguntas[rodada], True, branco)
        texto_rodada = fonte.render(
            f"Rodada {rodada + 1} de {total_rodadas}", True, branco)

        tela.blit(texto_tempo, (50, 520))
        tela.blit(texto_vidas, (500, 520))
        tela.blit(texto_pergunta, (300, 520))
        tela.blit(texto_rodada, (260, 560))
    else:
        texto_fim = fonte.render("Game Over", True, vermelho)
        tela.blit(texto_fim, (400, 300))
        pygame.display.flip()
        pygame.time.delay(2000)
        rodar = False

    for linha in desenhar_matriz:
        for bloco_data in linha:
            bloco_rect, cor_do_bloco, texto_bloco = bloco_data
            pygame.draw.rect(tela, cor_do_bloco, bloco_rect)
            texto_render = fonte.render(str(texto_bloco), True, numero_cor)
            texto_rect = texto_render.get_rect(center=bloco_rect.center)
            tela.blit(texto_render, texto_rect)

    pygame.display.flip()

pygame.quit()
