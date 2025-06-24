import pygame
import random

import config

def executar(callback_menu):
    # === CONFIGURAÇÃO GERAL ===
    largura, altura = 800, 600
    linhas, colunas = 5, 6
    largura_bloco, altura_bloco, espaco = 80, 80, 10
    margem_x = (largura - (colunas * (largura_bloco + espaco))) // 2
    margem_y = 80
    cores = {
        "rosa": (255, 0, 128), "vermelho": (255, 0, 0), "verde": (0, 255, 0),
        "azul": (0, 0, 255), "roxo": (128, 0, 128), "laranja": (255, 165, 0),
        "branco": (255, 255, 255), "preto": (0, 0, 0)
    }

    # === EXPRESSÕES MATEMÁTICAS ===
    def gerarOperacao(operador):
        tentativa = 0
        while tentativa < 100:
            if operador == '+':
                a, b = random.randint(5, 20), random.randint(5, 20)
                if a == b or a + b <= 10: tentativa += 1; continue
                return f"{a} + {b}", a + b
            if operador == '-':
                a, b = random.randint(5, 20), random.randint(1, 20)
                if a <= b or a - b <= 3: tentativa += 1; continue
                return f"{a} - {b}", a - b
            if operador == '*':
                a, b = random.randint(2, 10), random.randint(2, 10)
                if a == b == 1: tentativa += 1; continue
                return f"{a} * {b}", a * b
            if operador == '/':
                b = random.randint(2, 10)
                r = random.randint(2, 10)
                return f"{b*r} ÷ {b}", r
        return None

    def gerarVariasOperacoes(qtd=30):
        operadores = ['+', '-', '*', '/']

        expressoes, contador = [], {op: 0 for op in operadores}
        tentativa_total = 0
        while len(expressoes) < qtd and tentativa_total < 1000:
            op = random.choice(operadores)
            resultado = gerarOperacao(op)
            tentativa_total += 1
            if resultado:
                expr, val = resultado
                if val not in [v for _, v in expressoes]:
                    expressoes.append((expr, val))
                    contador[op] += 1
        return expressoes
    
    def substituir_expressao_rodada(rodada, perguntas, respostas):
        nova_expr = None
        tentativas = 0
        while not nova_expr and tentativas < 100:
            nova_expr = gerarOperacao(random.choice(['+', '-', '*', '/']))
            if nova_expr and nova_expr[1] in respostas:
                nova_expr = None
            tentativas += 1
        if nova_expr:
            perguntas[rodada] = nova_expr[0]
            respostas[rodada] = nova_expr[1]
            return True
        return False



    # === FUNÇÕES DE DESENHO ===
    def desenhar_matriz(tela, fonte, matriz_valores, matriz_cores):
        for i in range(linhas):
            for j in range(colunas):
                x = margem_x + j * (largura_bloco + espaco)
                y = margem_y + i * (altura_bloco + espaco)
                pygame.draw.rect(tela, matriz_cores[i][j], (x, y, largura_bloco, altura_bloco))
                valor = matriz_valores[i][j]
                texto = fonte.render(str(valor), True, cores["branco"])
                tela.blit(texto, texto.get_rect(center=(x + largura_bloco // 2, y + altura_bloco // 2)))

    def desenhar_jogador(tela, linha, coluna):
        px = margem_x + coluna * (largura_bloco + espaco) + largura_bloco // 2
        py = margem_y + linha * (altura_bloco + espaco) + altura_bloco // 2
        pygame.draw.circle(tela, (50, 50, 50), (px + 2, py + 2), 15)  # sombra
        pygame.draw.circle(tela, cores["preto"], (px, py), 18)       # borda
        pygame.draw.circle(tela, (0, 255, 255), (px, py), 15)         # bolinha

    def gerar_matriz_valores(expressoes):
        valores = list(set(val for _, val in expressoes))
        while len(valores) < linhas * colunas:
            novo = random.randint(2, 100)
            if novo not in valores: valores.append(novo)
        random.shuffle(valores)
        return [[valores[i * colunas + j] for j in range(colunas)] for i in range(linhas)]

    # === INICIALIZAÇÃO DO JOGO ===
    pygame.init()
    tela = pygame.display.set_mode((largura, altura))
    pygame.display.set_caption("JOGO BLOCOS - Expressões")
    fonte = pygame.font.Font(None, 36)
    fonte_grande = pygame.font.Font(None, 84)
    som_acerto = pygame.mixer.Sound("sons/acerto.mp3")
    som_erro = pygame.mixer.Sound("sons/erro.mp3")
    iconeimg = pygame.image.load("img/icone.png")
    pygame.display.set_icon(iconeimg)

    expressoes = gerarVariasOperacoes(30)
    perguntas = [e for e, _ in expressoes[:config.total_rodada]]
    respostas = [r for _, r in expressoes[:config.total_rodada]]
    matriz_valores = gerar_matriz_valores(expressoes)
    matriz_cores = [[random.choice(list(cores.values())[:6]) for _ in range(colunas)] for _ in range(linhas)]

    jogador_linha, jogador_coluna = 0, 0
    vidas, rodada = 3, 0
    tempo_limite = config.tempo_limite
    tempo_inicial = pygame.time.get_ticks()
    pausado = False
    mensagem, tempo_mensagem = "", 0
    clock = pygame.time.Clock()


    # === LOOP PRINCIPAL ===

    rodar = True
    while rodar:
        tela.fill(cores["preto"])
        tempo_atual = pygame.time.get_ticks()
        if not pausado:
            tempo_decorrido = (tempo_atual - tempo_inicial) / 1000
        else:
            tempo_decorrido = 0
        tempo_restante = max(0, tempo_limite - tempo_decorrido)

        # === BARRA DE TEMPO ===
        barra_x = 32
        barra_y = 22
        barra_largura_total = 200
        barra_altura = 20

        proporcao = tempo_restante / tempo_limite if tempo_limite > 0 else 0
        barra_largura_atual = int(barra_largura_total * proporcao)

        pygame.draw.rect(tela, (60, 60, 60), (barra_x, barra_y, barra_largura_total, barra_altura))
        pygame.draw.rect(tela, cores["verde"], (barra_x, barra_y, barra_largura_atual, barra_altura))

        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:
                rodar = False
            if evento.type == pygame.KEYDOWN:
                if evento.key == pygame.K_UP and jogador_linha > 0: jogador_linha -= 1
                if evento.key == pygame.K_DOWN and jogador_linha < linhas - 1: jogador_linha += 1
                if evento.key == pygame.K_LEFT and jogador_coluna > 0: jogador_coluna -= 1
                if evento.key == pygame.K_RIGHT and jogador_coluna < colunas - 1: jogador_coluna += 1

        if tempo_restante == 0 and rodada < len(perguntas) and vidas > 0:
            valor = matriz_valores[jogador_linha][jogador_coluna]
            if valor == respostas[rodada]:
                mensagem = "ACERTOU!"
                if config.som_ativo:
                    som_acerto.play()
                rodada += 1
            else:
                mensagem = "ERROU!"
                if config.som_ativo:
                    som_erro.play()
                vidas -= 1
                if substituir_expressao_rodada(rodada, perguntas, respostas):
                    matriz_valores = gerar_matriz_valores([(perguntas[rodada], respostas[rodada])])
            pausado = True
            tempo_inicial = pygame.time.get_ticks()
            tempo_mensagem = tempo_atual

        if mensagem:
            if tempo_atual - tempo_mensagem > 1000:
                mensagem = ""
                pausado = False
                tempo_inicial = pygame.time.get_ticks()

        desenhar_matriz(tela, fonte, matriz_valores, matriz_cores)
        desenhar_jogador(tela, jogador_linha, jogador_coluna)

        # Info: tempo, expressao, vidas
        tela.blit(fonte.render(f"Tempo: {tempo_restante:.0f}", True, cores["branco"]), (largura//2 - 60, 20))
        if rodada < len(perguntas):
            texto_expr = fonte.render(perguntas[rodada], True, cores["preto"])
            rect_expr = texto_expr.get_rect(center=(largura // 2, altura - 35))
            pygame.draw.rect(tela, cores["branco"], rect_expr.inflate(20, 10))

            tela.blit(texto_expr, rect_expr)

        tela.blit(fonte.render(f"Vidas: {vidas}", True, cores["branco"]), (20, altura - 40))
        tela.blit(fonte.render(f"Rodada {rodada+1} de {config.total_rodada}", True, cores["branco"]), (largura - 200, altura - 40))

        if mensagem:
        # Superfície semitransparente
            overlay = pygame.Surface((largura, altura), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # preto com 180 de transparência
            tela.blit(overlay, (0, 0))

            # Renderiza a mensagem
            texto_msg = fonte_grande.render(mensagem, True, cores["branco"])
            rect_msg = texto_msg.get_rect(center=(largura // 2, altura // 2))
            tela.blit(texto_msg, rect_msg)

        if rodada >= len(perguntas) or vidas <= 0:
            fim = "Parabéns! Você venceu!" if vidas > 0 else "Você perdeu!"
            cor_fundo = (0, 100, 0) if vidas > 0 else (100, 0, 0)
            cor_texto = cores["branco"]

            def reiniciar_jogo():
                nonlocal jogador_linha, jogador_coluna, vidas, rodada, tempo_inicial
                nonlocal pausado, expressoes, perguntas, respostas, matriz_valores, matriz_cores
                nonlocal mensagem, tempo_mensagem

                # Reinicia as variáveis do jogo
                jogador_linha, jogador_coluna = 0, 0
                vidas, rodada = 3, 0
                tempo_inicial = pygame.time.get_ticks()
                pausado = False
                expressoes = gerarVariasOperacoes(30)
                perguntas = [e for e, _ in expressoes[:config.total_rodada]]
                respostas = [r for _, r in expressoes[:config.total_rodada]]
                matriz_valores = gerar_matriz_valores(expressoes)
                matriz_cores = [[random.choice(list(cores.values())[:6]) for _ in range(colunas)] for _ in range(linhas)]
                mensagem, tempo_mensagem = "", 0

            while True:
                tela.fill(cor_fundo)

                # Mensagem de fim
                texto = fonte_grande.render(fim, True, cor_texto)
                tela.blit(texto, texto.get_rect(center=(largura // 2, altura // 2 - 120)))

                # Botão Jogar Novamente
                botao_novamente = pygame.Rect(largura // 2 - 125, altura // 2, 250, 60)
                pygame.draw.rect(tela, cores["branco"], botao_novamente)
                texto_novo = fonte.render("Jogar Novamente", True, cores["preto"])
                tela.blit(texto_novo, texto_novo.get_rect(center=botao_novamente.center))

                # Botão Voltar ao Menu
                botao_menu = pygame.Rect(largura // 2 - 125, altura // 2 + 80, 250, 60)
                pygame.draw.rect(tela, cores["branco"], botao_menu)
                texto_novo = fonte.render("Voltar ao Menu", True, cores["preto"])
                tela.blit(texto_novo, texto_novo.get_rect(center=botao_menu.center))

                # Botão Sair
                botao_sair = pygame.Rect(largura // 2 - 125, altura // 2 + 160, 250, 60)
                pygame.draw.rect(tela, cores["branco"], botao_sair)
                texto_sair = fonte.render("Sair", True, cores["preto"])
                tela.blit(texto_sair, texto_sair.get_rect(center=botao_sair.center))

                clock.tick(60)

                pygame.display.flip()

                for evento in pygame.event.get():
                    if evento.type == pygame.QUIT:
                        rodar = False
                        pygame.quit()
                        exit()
                    
                    if evento.type == pygame.MOUSEBUTTONDOWN:
                        if botao_novamente.collidepoint(evento.pos):
                            reiniciar_jogo()
                            break  # volta para o loop principal

                        if botao_menu.collidepoint(evento.pos):
                            reiniciar_jogo()
                            callback_menu()
                            return

                        if botao_sair.collidepoint(evento.pos):
                            rodar = False
                            pygame.quit()
                            exit()
                else:
                    continue
                break

        pygame.display.flip()

pygame.quit()